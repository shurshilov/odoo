# Copyright 2019 Artem Shurshilov
# Odoo Proprietary License v1.0

# This software and associated files (the "Software") may only be used (executed,
# modified, executed after modifications) if you have purchased a valid license
# from the authors, typically via Odoo Apps, or if you have received a written
# agreement from the authors of the Software (see the COPYRIGHT file).

# You may develop Odoo modules that use the Software as a library (typically
# by depending on it, importing it and using its resources), but without copying
# any source code or material from the Software. You may distribute those
# modules under the license of your choice, provided that this license is
# compatible with the terms of the Odoo Proprietary License (For example:
# LGPL, MIT, or proprietary licenses similar to this one).

# It is forbidden to publish, distribute, sublicense, or sell copies of the Software
# or modified copies of the Software.

# The above copyright notice and this permission notice must be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import base64
import io
from odoo import models, fields, api, registry

# from . import classify
# from . import preprocess
import sys
import cv2
import time

# from scipy import misc
import os
from PIL import Image
import base64

# from imutils.video import FileVideoStream
# from imutils.video import FPS
from datetime import datetime
import threading
import logging

_logger = logging.getLogger(__name__)


class FaceIdNotification(models.Model):
    _name = "faceid.notification"
    _inherit = ["mail.thread"]
    _description = "Notifications list"

    name = fields.Char(string="Name of notification")
    state = fields.Selection(
        [("off", "Off"), ("on", "On")],
        string="State (enable/disable)",
        default="off",
    )
    type = fields.Selection(
        [("email", "Email"), ("sms", "Sms")],
        string="Type notification",
        default="email",
    )
    action = fields.Selection(
        [
            ("off", "Camera off"),
            ("black", "Face from Black list found"),
            ("employee", "Employee found"),
        ],
        string="Action to send",
        default="off",
    )
    template_id = fields.Many2one(
        "mail.template",
        string="Email Template",
        domain=[("model", "=", "faceid.notification")],
        ondelete="restrict",
        help="This field contains the template of the mail that will be automatically sent",
        required=True,
    )
    source_id = fields.Many2one(
        comodel_name="faceid.source", string="Source link", required=True
    )
    count_send_setting = fields.Integer(
        string="Send Counter settings", default=1
    )
    count_send_real = fields.Integer(string="Send Counter", default=1)

    @api.model
    def send_email(self):
        # only email and enable
        for rec in self.search([("state", "=", "on"), ("type", "=", "email")]):
            # if not sended
            if rec.count_send_real > 0:
                camera = self.env["faceid.source"].browse(rec.source_id.id)
                name = "terminator_" + str(camera.id)
                # if camera is off recognize
                if not len(
                    [
                        s
                        for s in [str(i) for i in threading.enumerate()]
                        if name in s
                    ]
                ):
                    # send message camera_off
                    rec.count_send_real = rec.count_send_real - 1
                    template_browse = self.env["mail.template"].browse(
                        rec.template_id.id
                    )
                    template_browse.send_mail(rec.id, force_send=True)


class FaceIdAction(models.Model):
    _name = "faceid.action"
    _description = "Human faces list"

    name = fields.Char(string="Name of action")
    face = fields.Binary(string="Found face")
    face_id = fields.Many2one(
        comodel_name="faceid.action", string="Ближайшая запись"
    )
    face_id_image = fields.Binary(
        related="face_id.face", string="Ближайшее лицо фото"
    )
    min_distanse = fields.Float(string="Min distanse", default=101)
    unique = fields.Boolean(
        string="Unique", compute="_compute_unique", store=True
    )
    source_id = fields.Many2one(
        comodel_name="faceid.source", string="Source link"
    )

    @api.model
    def create(self, values):
        rec = super().create(values)
        if rec.min_distanse >= rec.source_id.recognize_threshold:
            rec.unique = True
        else:
            rec.unique = False
        return rec

    # @api.multi
    # @api.depends('source_id')
    def _compute_unique(self):
        for rec in self:
            _logger.warning("!!!!!!!!!!")
            _logger.warning(rec.min_distanse)
            _logger.warning(rec.source_id.recognize_threshold)
            if rec.min_distanse >= rec.source_id.recognize_threshold:
                rec.unique = True
            else:
                rec.unique = False


class FaceIdSource(models.Model):
    _name = "faceid.source"
    _description = "Camera interface"

    name = fields.Char(string="Name of location camera")
    url = fields.Char(string="Source url")
    faces = fields.One2many(
        "faceid.action",
        "source_id",
        string="Found actions",
        domain=[("create_date", ">=", datetime.today().strftime("%Y-%m-%d"))],
    )
    frame_interval = fields.Integer(string="Frame interval", default=10)
    min_size = fields.Integer(string="Min size face, px", default=90)
    scaled = fields.Float(string="Scale algo", default=1.15)
    x = fields.Integer(string="X coords", default=0)
    y = fields.Integer(string="Y coords", default=0)
    height = fields.Integer(string="height", default=0)
    width = fields.Integer(string="width", default=0)
    speed_detect = fields.Integer(string="Speed face detect, ms", default=0)
    recognize_threshold = fields.Float(
        string="Recognize threshold", default=0.8
    )
    state_compute = fields.Selection(
        [("off", "Off"), ("on", "On")],
        string="State compute",
        compute="_compute_state",
    )
    state = fields.Selection(
        [("off", "Off"), ("on", "On")],
        string="Status",
        readonly=True,
        copy=False,
        default="off",
        store=True,
        related="state_compute",
    )
    faces_count_today = fields.Integer(
        compute="_compute_faces_count_today",
        string="Faces Count",
        type="integer",
    )
    faces_count_all = fields.Integer(
        compute="_compute_faces_count_all", string="Faces Count", type="integer"
    )
    pid = fields.Char(string="PID thread")

    # api.multi
    def _compute_faces_count_all(self):
        FaceidAction = self.env["faceid.action"]
        for rec in self:
            rec.faces_count_all = FaceidAction.search_count([])

    # @api.multi
    def _compute_faces_count_today(self):
        FaceidAction = self.env["faceid.action"]
        for rec in self:
            rec.faces_count_today = FaceidAction.search_count(
                [
                    ("source_id", "=", rec.id),
                    ("create_date", ">=", datetime.now().strftime("%Y-%m-%d")),
                ]
            )

    # @api.multi
    def _compute_state(self):
        for rec in self:
            _logger.warning(str([str(i) for i in threading.enumerate()]))
            name = "terminator_" + str(rec.id)
            if len(
                [
                    s
                    for s in [str(i) for i in threading.enumerate()]
                    if name in s
                ]
            ):
                rec.state_compute = "on"
            else:
                rec.state_compute = "off"

    def save_face_odoo(self, filename, image, min_dist, face_id):
        """[Save founded image to camera record field 'faces']

        [Just save to DB]

        Arguments:
            filename {[type]} -- [filename to save]
            image {[type]} -- [foto]
        """

        img = Image.fromarray(image)
        with io.BytesIO() as buffered:
            img.save(buffered, format=img.format) if img.format else img.save(
                buffered, format="PNG"
            )
            img_str = base64.b64encode(buffered.getvalue())
            action = self.env["faceid.action"].create(
                {
                    "face": img_str,
                    "name": self.name,
                    "min_distanse": min_dist,
                    "source_id": self.id,
                }
            )
            self._cr.commit()
            if face_id == -1:
                action.face_id = action.id
            else:
                action.face_id = face_id
            self._cr.commit()
            self.faces = [(4, action.id)]
            self._cr.commit()
            # self.env.cr.commit()

    # @api.multi
    def stop_detec_face(self):
        config_parameters = self.env["ir.config_parameter"]
        config_parameters.set_param("faceid_thread_" + str(self.id), 0)

    # @api.multi
    def detec_face_thread(self):
        """[Button click user 'Start']

        [Start terminator bots]

        Decorators:
            api.multi

        Returns:
            bool -- [description]
        """
        for rec in self:
            listm = self.env["faceid.notification"].search(
                [("source_id.id", "=", rec.id)]
            )
            for notify in listm:
                notify.count_send_real = notify.count_send_setting
            thread_var = threading.Thread(target=rec.terminator_eye, args=())
            _logger.warning(str(thread_var))
            _logger.warning(str(threading.enumerate()))
            thread_var.daemon = False
            thread_var.setName("terminator_" + str(rec.id))
            thread_var.start()
        return True

    def reset_attempts(self):
        """[Count reconnect to camera]

        Returns:
            number -- [description]
        """
        return 50

    def detection_and_recognize(self, camera, attempts):
        rec = self
        # rec = self.with_env(new_env)
        odoo_path = "\\".join(os.path.abspath(__file__).split("\\")[:-1]) + "\\"
        preprocessor = preprocess.PreProcessor(rec.min_size, rec.scaled)
        i, start, id = 0, time.time(), str(rec.id)
        y, x, h, w, dt = rec.y, rec.x, rec.height, rec.width, 0
        threshold = rec.recognize_threshold
        classifier = classify.Classify(_logger)
        while True:
            cv2.waitKey(1)
            ok, frame = camera.read()
            if not ok:
                _logger.warning("Disconnected faceid.source = " + id)
                camera.release()
                if attempts > 0:
                    time.sleep(5)
                    return True
                else:
                    return False

            if i % rec.frame_interval == 0:
                # try:
                if y == 0 and x == 0 and h == 0 and w == 0:
                    pass
                else:
                    frame = frame[y : y + h, x : x + w]
                # 4 АЛГОРИТМ MTCNN
                t = time.time()
                preprocessor.filename = "1.png"
                bb = preprocessor.align(frame, _logger)
                dt = time.time() - t

                if bb.any():
                    cv2.rectangle(
                        frame, (bb[0], bb[1]), (bb[2], bb[3]), (0, 255, 0), 5
                    )

                if preprocessor.filename != "1.png":
                    _logger.warning("min_dist")
                    self._cr.commit()
                    rec.faces.filtered(
                        lambda r: r.create_date.strftime("%Y-%m-%d")
                        == datetime.now().strftime("%Y-%m-%d")
                    )
                    list_images = rec.mapped("faces.face")
                    list_ids = rec.mapped("faces.id")
                    # list_images = [j.face for j in rec.faces if j.create_date.strftime("%Y-%m-%d") == datetime.now().strftime("%Y-%m-%d")]
                    _logger.warning("min_dist1")
                    _logger.warning("classifier")
                    # min_dist, id = classifier.predict_odoo(odoo_path + 'temp.png', list_images , _logger, list_ids)
                    min_dist, id = classifier.predict_odoo(
                        preprocessor.scaled, list_images, _logger, list_ids
                    )
                    # classifier.sess.close()
                    _logger.warning("min_dist2")
                    _logger.warning(min_dist)
                    # [new] если похожего лица нет в базе
                    if min_dist >= threshold:
                        rec.save_face_odoo(
                            preprocessor.filename,
                            preprocessor.scaled,
                            min_dist,
                            -1,
                        )
                    else:
                        rec.save_face_odoo(
                            preprocessor.filename,
                            preprocessor.scaled,
                            min_dist,
                            id,
                        )
                    _logger.warning("FPS" * 30)
                    _logger.warning(dt)
            # except Exception as e:
            #    _logger.warning(str(e))
            #    _logger.warning('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))

            i += 1
            # if(i % 1000 == 0):
            # rec.speed_detect = int(dt)
            # rec.env.cr.commit()
        camera.release()
        return False

    # @api.multi
    def terminator_eye(self):
        """[Terminator BOT]

        [This func try get image from camera (url) in loops and
        and can reconnect a given number of times.
        In addition, all this happens in a new thread,
        in which a new environment and therefore the response
        for the user occurs instantly, but in fact the face
        search engine is constantly running until it is
        stopped manually or the server is not restarted]

        Decorators:
            api.multi
        """
        with api.Environment.manage():
            # As this function is in a new thread, I need to open a new cursor, because the old one may be closed
            # new_cr = odoo.sql_db.db_connect(self.env.cr.dbname).cursor()
            uid, context, ids = self.env.uid, self.env.context, self.ids
            with api.Environment.manage():
                # self.env = api.Environment(new_cr, uid, context)
                # new_env = api.Environment(new_cr, uid, context)
                try:
                    with registry(self._cr.dbname).cursor() as cr:
                        env = api.Environment(cr, uid, context)
                        for rec in env["faceid.source"].search(
                            [("id", "in", ids)]
                        ):
                            rec._cr.commit()
                            _logger.warning(str(rec))
                            recall = True
                            attempts = self.reset_attempts()
                            while recall:
                                rec._cr.commit()
                                if not rec.url:
                                    camera = cv2.VideoCapture(0)
                                else:
                                    camera = cv2.VideoCapture(rec.url)
                                    rec._cr.commit()
                                if camera.isOpened():
                                    recall = rec.detection_and_recognize(
                                        camera, attempts
                                    )
                                    rec._cr.commit()
                                    attempts -= 1
                                else:
                                    _logger.warning(
                                        "Camera not opened "
                                        + datetime.now().strftime(
                                            "%m-%d-%Y %I:%M:%S%p"
                                        )
                                    )
                                    camera.release()
                                    attempts -= 1
                                    _logger.warning(
                                        "attempts: " + str(attempts)
                                    )
                                    # give the camera some time to recover
                                    time.sleep(5)
                                    continue
                except Exception as e:
                    _logger.warning("New cursor of thread closed")
                    _logger.info(
                        "Error on line {}".format(sys.exc_info()[-1].tb_lineno)
                    )
                    _logger.warning(str(e))
                    self._cr.close()
                    # self.env.cr.close()
