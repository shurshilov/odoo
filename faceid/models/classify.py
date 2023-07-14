import tensorflow as tf
import imageio
import numpy as np
import os
import math
import re
import base64
import io
from PIL import Image


class Classify:
    def __init__(self, _logger):
        # tf.logging.set_verbosity(tf.logging.INFO)
        # tf_logger = tf_logging._get_logger()
        # tf_logger.handlers = [_logger]
        # gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.85)
        # self.sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options, log_device_placement=True)).__enter__()
        self.sess = tf.compat.v1.Session().__enter__()
        self.odoo_path = (
            "\\".join(os.path.abspath(__file__).split("\\")[:-1]) + "\\"
        )
        self.load_model(self.odoo_path + "models")
        self.images_placeholder = (
            tf.compat.v1.get_default_graph().get_tensor_by_name("input:0")
        )
        self.embeddings = tf.compat.v1.get_default_graph().get_tensor_by_name(
            "embeddings:0"
        )
        self.phase_train_placeholder = (
            tf.get_default_graph().get_tensor_by_name("phase_train:0")
        )
        self.embedding_size = self.embeddings.get_shape()[1]
        self.emb_array = np.zeros((1, self.embedding_size))

        # classifier_filename_exp = os.path.expanduser(self.odoo_path + "classifier.pk")
        # with open(classifier_filename_exp, 'rb') as infile:
        #     (self.model, self.class_names) = pickle.load(infile)

    # def __del__(self):
    #    self.sess.close()

    def array_to_image(self, array):
        img = Image.fromarray(array)
        with io.BytesIO() as buffered:
            img.save(buffered, format=img.format) if img.format else img.save(
                buffered, format="PNG"
            )
            return buffered.getvalue()

    def predict_odoo(self, image_compare, images_list, logger, list_ids):
        # try:
        with self.sess.as_default() as sess:
            # with tf.Session() as sess:
            self.sess = sess
            # преобразуем base64 в реальные файлы
            logger.info(len(images_list))
            real_images = []
            for image in images_list:
                real_images.append(
                    self.load_images(io.BytesIO(base64.b64decode(image)))
                )
            # real_images.append(self.load_images(image_compare))
            real_images.append(
                self.load_images(self.array_to_image(image_compare))
            )
            np_images = np.stack(real_images)

            logger.info("NE0")
            logger.info(self.embeddings.get_shape()[1])

            nrof_images = len(np_images)
            nrof_batches_per_epoch = int(math.ceil(1.0 * nrof_images / 18))
            self.emb_array = np.zeros((nrof_images, self.embedding_size))
            # self.emb_array = np.zeros((nrof_images, nrof_images))
            for i in range(nrof_batches_per_epoch):
                start_index = i * 18
                end_index = min((i + 1) * 18, nrof_images)
                images = np_images[start_index:end_index]
                feed_dict = {
                    self.images_placeholder: images,
                    self.phase_train_placeholder: False,
                }
                logger.info("Before recognize")
                logger.info(start_index)
                logger.info(end_index)
                self.emb_array[start_index:end_index, :] = self.sess.run(
                    self.embeddings, feed_dict=feed_dict
                )
            logger.info("NE")

            # сравнение дистанций (такое лицо уже есть в базе или нет)
            nrof_images = len(self.emb_array)
            logger.info(nrof_images)
            logger.info(len(list_ids))
            logger.info(list_ids)
            min_dist = 100
            id = False
            for j in range(nrof_images - 1):
                dist = np.sqrt(
                    np.sum(
                        np.square(
                            np.subtract(
                                self.emb_array[nrof_images - 1, :],
                                self.emb_array[j, :],
                            )
                        )
                    )
                )
                if dist < min_dist:
                    min_dist = dist
                    id = list_ids[j]
            return min_dist, id

    # except Exception as e:
    #    logger.info('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
    #    logger.info(str(e))
    #    return 100, False

    def predict_db(self, path, db_path):
        # берем все картинки из папки с базой данных
        images = os.listdir(db_path)
        images_all = []
        for image in images:
            images_all.append(db_path + image)

        # также добавляем текущую картинку
        images_all.append(path)

        # преобразуем пути в реальные файлы
        real_images = []
        for image in images_all:
            real_images.append(self.load_images(image))

        real_images = np.stack(real_images)

        self.feed_dict = {
            self.images_placeholder: real_images,
            self.phase_train_placeholder: False,
        }

        # отработка нейросети
        self.emb_array = self.sess.run(
            self.embeddings, feed_dict=self.feed_dict
        )

        # сравнение дистанций (такое лицо уже есть в базе или нет)
        nrof_images = len(real_images)
        min_dist = 100
        for j in range(nrof_images - 1):
            dist = np.sqrt(
                np.sum(
                    np.square(
                        np.subtract(
                            self.emb_array[nrof_images - 1, :],
                            self.emb_array[j, :],
                        )
                    )
                )
            )
            if dist < min_dist:
                min_dist = dist
        return min_dist

    def predict(self, path):
        image = self.load_image(path)
        self.feed_dict = {
            self.images_placeholder: image,
            self.phase_train_placeholder: False,
        }
        self.emb_array[0, :] = self.sess.run(
            self.embeddings, feed_dict=self.feed_dict
        )
        predictions = self.model.predict_proba(self.emb_array)
        best_class_indices = np.argmax(predictions, axis=1)
        best_class_probabilities = predictions[
            np.arange(len(best_class_indices)), best_class_indices
        ]

        if best_class_probabilities[0] < 0.8:
            return "Unknown face"
        else:
            return self.class_names[best_class_indices[0]]

    def prewhiten(self, x):
        mean = np.mean(x)
        std = np.std(x)
        std_adj = np.maximum(std, 1.0 / np.sqrt(x.size))
        y = np.multiply(np.subtract(x, mean), 1 / std_adj)
        return y

    def load_image(self, image_path):
        image = np.zeros((1, 160, 160, 3))
        img = imageio.imread(image_path)
        img = self.prewhiten(img)
        image[0, :, :, :] = img
        return

    def load_images(self, image_path):
        # image = np.zeros((1, 160, 160, 3))
        img = imageio.imread(image_path)
        img = self.prewhiten(img)
        # image[0,:,:,:] = img
        # return image
        return img

    def load_model(self, model="./model"):
        model_exp = os.path.expanduser(model)
        print("Model directory: %s" % model_exp)
        meta_file, ckpt_file = self.get_model_filenames(model_exp)

        print("Metagraph file: %s" % meta_file)
        print("Checkpoint file: %s" % ckpt_file)

        self.saver = tf.compat.v1.train.import_meta_graph(
            os.path.join(model_exp, meta_file), input_map=None
        )
        self.saver.restore(
            tf.compat.v1.get_default_session(),
            os.path.join(model_exp, ckpt_file),
        )

    def get_model_filenames(self, model_dir):
        files = os.listdir(model_dir)
        meta_files = [s for s in files if s.endswith(".meta")]
        if len(meta_files) == 0:
            raise ValueError(
                "No meta file found in the model directory (%s)" % model_dir
            )
        elif len(meta_files) > 1:
            raise ValueError(
                "There should not be more than one meta file in the model directory (%s)"
                % model_dir
            )
        meta_file = meta_files[0]
        ckpt = tf.train.get_checkpoint_state(model_dir)
        if ckpt and ckpt.model_checkpoint_path:
            ckpt_file = os.path.basename(ckpt.model_checkpoint_path)
            return meta_file, ckpt_file

        meta_files = [s for s in files if ".ckpt" in s]
        max_step = -1
        for f in files:
            step_str = re.match(r"(^model-[\w\- ]+.ckpt-(\d+))", f)
            if step_str is not None and len(step_str.groups()) >= 2:
                step = int(step_str.groups()[1])
                if step > max_step:
                    max_step = step
                    ckpt_file = step_str.groups()[0]
        return meta_file, ckpt_file
