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

from odoo import api, fields, models


class ResConfigSettingsIapFirebase(models.TransientModel):
    _inherit = "res.config.settings"

    mail_firebase_key = fields.Char(
        string="Mail Firebase key", help="Secret firebase key"
    )
    mail_firebase_apiKey = fields.Char(
        string="Mail Firebase apiKey", help="Secret firebase apiKey"
    )
    mail_firebase_authDomain = fields.Char(
        string="Mail Firebase authDomain", help="Secret firebase authDomain"
    )
    mail_firebase_databaseURL = fields.Char(
        string="Mail Firebase databaseURL", help="Secret firebase databaseURL"
    )
    mail_firebase_projectId = fields.Char(
        string="Mail Firebase projectId", help="Secret firebase projectId"
    )
    mail_firebase_storageBucket = fields.Char(
        string="Mail Firebase storageBucket",
        help="Secret firebase storageBucket",
    )
    mail_firebase_messagingSenderId = fields.Char(
        string="Mail Firebase messagingSenderId",
        help="Secret firebase messagingSenderId",
    )
    mail_firebase_appId = fields.Char(
        string="Mail Firebase appId", help="Secret firebase appId"
    )
    mail_firebase_measurementId = fields.Char(
        string="Mail Firebase measurementId",
        help="Secret firebase measurementId",
    )

    def set_values(self):
        res = super().set_values()
        config_parameters = self.env["ir.config_parameter"]
        config_parameters.set_param("mail_firebase_key", self.mail_firebase_key)
        config_parameters.set_param(
            "mail_firebase_apiKey", self.mail_firebase_apiKey
        )
        config_parameters.set_param(
            "mail_firebase_authDomain", self.mail_firebase_authDomain
        )
        config_parameters.set_param(
            "mail_firebase_databaseURL", self.mail_firebase_databaseURL
        )
        config_parameters.set_param(
            "mail_firebase_projectId", self.mail_firebase_projectId
        )
        config_parameters.set_param(
            "mail_firebase_storageBucket", self.mail_firebase_storageBucket
        )
        config_parameters.set_param(
            "mail_firebase_messagingSenderId",
            self.mail_firebase_messagingSenderId,
        )
        config_parameters.set_param(
            "mail_firebase_appId", self.mail_firebase_appId
        )
        config_parameters.set_param(
            "mail_firebase_measurementId", self.mail_firebase_measurementId
        )
        return res

    @api.model
    def get_values(self):
        res = super().get_values()
        res.update(
            mail_firebase_key=self.env["ir.config_parameter"].get_param(
                "mail_firebase_key"
            )
        )
        res.update(
            mail_firebase_apiKey=self.env["ir.config_parameter"].get_param(
                "mail_firebase_apiKey"
            )
        )
        res.update(
            mail_firebase_authDomain=self.env["ir.config_parameter"].get_param(
                "mail_firebase_authDomain"
            )
        )
        res.update(
            mail_firebase_databaseURL=self.env["ir.config_parameter"].get_param(
                "mail_firebase_databaseURL"
            )
        )
        res.update(
            mail_firebase_projectId=self.env["ir.config_parameter"].get_param(
                "mail_firebase_projectId"
            )
        )
        res.update(
            mail_firebase_storageBucket=self.env[
                "ir.config_parameter"
            ].get_param("mail_firebase_storageBucket")
        )
        res.update(
            mail_firebase_messagingSenderId=self.env[
                "ir.config_parameter"
            ].get_param("mail_firebase_messagingSenderId")
        )
        res.update(
            mail_firebase_appId=self.env["ir.config_parameter"].get_param(
                "mail_firebase_appId"
            )
        )
        res.update(
            mail_firebase_measurementId=self.env[
                "ir.config_parameter"
            ].get_param("mail_firebase_measurementId")
        )
        return res
