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


class ResConfigSettingsOnedrive(models.TransientModel):
    _inherit = "res.config.settings"

    onedrive_client_id = fields.Char(
        string="Microsoft Onedrive client id", help="Set value from your Microsoft Azure account"
    )
    onedrive_viewType = fields.Char(
        string="Microsoft Onedrive viewtype (folders, files, all)", default="all"
    )
    onedrive_storage = fields.Selection(
        string="Storage files",
        selection=[("copy", "Copy to Odoo"), ("url", "Save url"), ("any", "Question user")],
        default="any",
    )

    def set_values(self):
        res = super().set_values()
        config_parameters = self.env["ir.config_parameter"]
        config_parameters.set_param("onedrive_client_id", self.onedrive_client_id)
        config_parameters.set_param("onedrive_viewType", self.onedrive_viewType)
        config_parameters.set_param("onedrive_storage", self.onedrive_storage)
        # config_parameters.set_param("gdrive_navbar_hidden", self.gdrive_navbar_hidden)
        # config_parameters.set_param("gdrive_locale", self.gdrive_locale)
        # config_parameters.set_param("gdrive_dir", self.gdrive_dir)
        return res

    @api.model
    def get_values(self):
        res = super().get_values()
        res.update(
            onedrive_client_id=self.env["ir.config_parameter"].get_param("onedrive_client_id")
        )
        res.update(onedrive_viewType=self.env["ir.config_parameter"].get_param("onedrive_viewType"))
        res.update(onedrive_storage=self.env["ir.config_parameter"].get_param("onedrive_storage"))
        # res.update(gdrive_navbar_hidden = self.env['ir.config_parameter'].get_param('gdrive_navbar_hidden'))
        # res.update(gdrive_locale = self.env['ir.config_parameter'].get_param('gdrive_locale'))
        # res.update(gdrive_dir = self.env['ir.config_parameter'].get_param('gdrive_dir'))
        return res
