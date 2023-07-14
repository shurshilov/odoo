# from scipy import misc
import tensorflow as tf
import numpy as np
from . import detect_face
import os
import datetime
import cv2


class PreProcessor:
    def __init__(self, minsize=20, scaled=0):
        with tf.Graph().as_default():
            # gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.85)
            # self.sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options, log_device_placement=False))
            self.sess = tf.compat.v1.Session()
            with self.sess.as_default():
                self.pnet, self.rnet, self.onet = detect_face.create_mtcnn(
                    self.sess, None
                )

            self.minsize = minsize  # minimum size of face
            self.threshold = [0.6, 0.7, 0.7]  # three steps's threshold
            self.factor = 0.709  # scale factor
            self.scaled = scaled
            self.filename = "1.png"
            self.odoo_path = (
                "\\".join(os.path.abspath(__file__).split("\\")[:-1]) + "\\"
            )

    def align(self, image, _logger, margin=44, image_size=160):
        img = image
        # img = img[:,:,0:3]
        bounding_boxes, _ = detect_face.detect_face(
            img,
            self.minsize,
            self.pnet,
            self.rnet,
            self.onet,
            self.threshold,
            self.factor,
            _logger,
        )
        nrof_faces = bounding_boxes.shape[0]
        bb = np.zeros(4, dtype=np.int32)
        if nrof_faces > 0:
            det = bounding_boxes[:, 0:4]
            img_size = np.asarray(img.shape)[0:2]
            if nrof_faces > 1:
                bounding_box_size = (det[:, 2] - det[:, 0]) * (
                    det[:, 3] - det[:, 1]
                )
                img_center = img_size / 2
                offsets = np.vstack(
                    [
                        (det[:, 0] + det[:, 2]) / 2 - img_center[1],
                        (det[:, 1] + det[:, 3]) / 2 - img_center[0],
                    ]
                )
                offset_dist_squared = np.sum(np.power(offsets, 2.0), 0)
                index = np.argmax(
                    bounding_box_size - offset_dist_squared * 2.0
                )  # some extra weight on the centering
                det = det[index, :]
        else:
            return bb

        det = np.squeeze(det)
        bb[0] = np.maximum(det[0] - margin / 2, 0)
        bb[1] = np.maximum(det[1] - margin / 2, 0)
        bb[2] = np.minimum(det[2] + margin / 2, img_size[1])
        bb[3] = np.minimum(det[3] + margin / 2, img_size[0])
        cropped = img[bb[1] : bb[3], bb[0] : bb[2], :]
        self.scaled = cv2.resize(
            cropped, (image_size, image_size), interpolation=cv2.INTER_LINEAR
        )
        # self.scaled = misc.imresize(cropped, (image_size, image_size), interp='bilinear')
        dt = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        self.filename = self.odoo_path + "db\\temp" + dt + ".png"
        # misc.imsave(self.odoo_path + "temp.png", self.scaled)
        cv2.imwrite(self.odoo_path + "temp.png", self.scaled)
        return bb
