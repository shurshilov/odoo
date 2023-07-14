# Copyright 2020 Artem Shurshilov
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

from odoo import fields, models, api
import requests


class CrmLead(models.Model):
    _inherit = "crm.lead"

    firebase_push_token = fields.Char(string="Device firebase token")


class CrmLeadFirebaseMessage(models.TransientModel):
    _name = "crm.lead.firebase.message"
    _description = "Wizard to send message to leads"

    title = fields.Char(
        string="Title firebase message",
        required=True,
        default=lambda self: self._get_default_title(),
    )
    body = fields.Char(
        string="Body firebase message",
        required=True,
        default=lambda self: self._get_default_body(),
    )
    icon = fields.Char(
        string="Icon URL firebase message",
        required=True,
        default=lambda self: self._get_default_icon(),
    )
    image = fields.Char(
        string="Image URL firebase message",
        required=True,
        default=lambda self: self._get_default_image(),
    )
    click_action = fields.Char(
        string="Action URL firebase message",
        required=True,
        default=lambda self: self._get_default_action(),
    )

    @api.model
    def _get_default_title(self):
        return (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("firebase_title_web")
        )

    @api.model
    def _get_default_body(self):
        return (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("firebase_body_web")
        )

    @api.model
    def _get_default_icon(self):
        return (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("firebase_icon_web")
        )

    @api.model
    def _get_default_image(self):
        return (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("firebase_image_web")
        )

    @api.model
    def _get_default_action(self):
        return (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("firebase_action_web")
        )

    def channel_firebase_notifications(self):
        """Wizard for send messages firebase device
        https://firebase.google.com/docs/cloud-messaging/http-server-ref"""
        lead_ids = self._context.get("active_ids")
        device_ids = (
            self.env["crm.lead"]
            .sudo()
            .search(
                [
                    ("id", "in", lead_ids),
                    ("firebase_push_token", "!=", False),
                ]
            )
            .mapped("firebase_push_token")
        )

        if len(device_ids) == 0:
            return

        key = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("mail_firebase_key")
        )
        if not key:
            return

        url = "https://fcm.googleapis.com/fcm/send"

        headers = {
            "Content-Type": "application/json",
            "Authorization": "key={}".format(key),
        }
        # https://eurodoo.com/cloud_companion/static/description/eurodoo.png
        # от 1 до 1000
        if len(device_ids) > 1:
            data = {
                "notification": {
                    "title": self.title,
                    "icon": self.icon,
                    "image": self.image,
                    "body": self.body,
                    "click_action": self.click_action,
                    "sound": None,
                    "badge": None,
                },
                "dry_run": False,  # test query
                "priority": "high",
                "content_available": True,
                "registration_ids": device_ids,
            }
        else:
            data = {
                "notification": {
                    "title": self.title,
                    "subtitle": self.title,
                    "icon": self.icon,
                    # 'image': self.image,
                    "body": self.body,
                    "click_action": self.click_action,
                    "sound": None,
                    "badge": None,
                },
                "dry_run": False,  # test query
                "priority": "high",
                "content_available": True,
                "to": ",".join(device_ids),
            }
        print(headers, data)
        answer = requests.post(url, json=data, headers=headers)
        print(answer.text)
