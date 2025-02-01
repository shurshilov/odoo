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

from odoo import api, fields, models


class ResConfigSettingsGDriveField(models.TransientModel):
    _inherit = "res.config.settings"

    gdrivef_client_id = fields.Char(
        string="Google drive client id",
        help="Set value from your Google account",
    )
    gdrivef_scope = fields.Char(
        string="Google drive scope",
        default="https://www.googleapis.com/auth/drive",
    )
    gdrivef_mimetypes = fields.Char(string="Google drive mimetypes")
    gdrivef_navbar_hidden = fields.Boolean(string="Google drive navbar hidden")
    gdrivef_locale = fields.Char(string="Google drive locale")
    gdrivef_dir = fields.Char(string="Google drive directory for upload in tab")
    gdrivef_storage = fields.Selection(
        string="Storage files",
        selection=[
            ("copy", "Copy to Odoo"),
            ("url", "Save url"),
            ("any", "Question user"),
        ],
        default="any",
    )

    def set_values(self):
        res = super().set_values()
        config_parameters = self.env["ir.config_parameter"]
        config_parameters.set_param("gdrivef_client_id", self.gdrivef_client_id)
        config_parameters.set_param("gdrivef_scope", self.gdrivef_scope)
        config_parameters.set_param("gdrivef_mimetypes", self.gdrivef_mimetypes)
        config_parameters.set_param(
            "gdrivef_navbar_hidden", self.gdrivef_navbar_hidden
        )
        config_parameters.set_param("gdrivef_locale", self.gdrivef_locale)
        config_parameters.set_param("gdrivef_dir", self.gdrivef_dir)
        config_parameters.set_param("gdrivef_storage", self.gdrivef_storage)
        return res

    @api.model
    def get_values(self):
        res = super().get_values()
        res.update(
            gdrivef_client_id=self.env["ir.config_parameter"].get_param(
                "gdrivef_client_id"
            )
        )
        res.update(
            gdrivef_scope=self.env["ir.config_parameter"].get_param(
                "gdrivef_scope"
            )
        )
        res.update(
            gdrivef_mimetypes=self.env["ir.config_parameter"].get_param(
                "gdrivef_mimetypes"
            )
        )
        res.update(
            gdrivef_navbar_hidden=self.env["ir.config_parameter"].get_param(
                "gdrivef_navbar_hidden"
            )
        )
        res.update(
            gdrivef_locale=self.env["ir.config_parameter"].get_param(
                "gdrivef_locale"
            )
        )
        res.update(
            gdrivef_dir=self.env["ir.config_parameter"].get_param("gdrivef_dir")
        )
        res.update(
            gdrivef_storage=self.env["ir.config_parameter"].get_param(
                "gdrivef_storage"
            )
        )
        return res
