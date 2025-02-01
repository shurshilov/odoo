# Copyright 2021-2022 Artem Shurshilov
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
from odoo.exceptions import ValidationError
import json
import base64


class ResConfigSettingsBackup(models.TransientModel):
    _inherit = "res.config.settings"

    abp_json_secret_file = fields.Binary("Json secret file")
    abp_credentials = fields.Char("Credentials")
    abp_token = fields.Char("Access Token")

    def get_credentials(self):
        return {
            "type": "ir.actions.act_url",
            "name": "Auto backup pro authorize",
            "url": "/authorize_auto_backup_grive",
            "target": "new",
        }

    def set_values(self):
        res = super().set_values()
        self.env["ir.config_parameter"].set_param(
            "abp_json_secret_file",
            json.loads(base64.b64decode(self.abp_json_secret_file)),
        )
        return res

    @api.model
    def get_values(self):
        res = super().get_values()
        if self.env["ir.config_parameter"].get_param("abp_json_secret_file"):
            try:
                json_secret_file = base64.b64encode(
                    json.dumps(
                        self.env["ir.config_parameter"].get_param(
                            "abp_json_secret_file"
                        )
                    ).encode("utf-8")
                )
                res.update(abp_json_secret_file=json_secret_file)
            except Exception:
                raise ValidationError("Error parse client json file")
        res.update(
            abp_credentials=self.env["ir.config_parameter"].get_param(
                "abp_credentials"
            )
        )
        res.update(
            abp_token=self.env["ir.config_parameter"].get_param("abp_token")
        )

        return res
