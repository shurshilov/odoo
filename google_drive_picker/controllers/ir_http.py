# Copyright (C) 2020 Artem Shurshilov <shurshilov.a@yandex.ru>
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
from odoo import models


class Http(models.AbstractModel):
    _inherit = "ir.http"

    def session_info(self):
        """Params for dynamic interface"""
        result = super().session_info()
        # env = request.env['ir.config_parameter'].sudo()
        env = self.env["ir.config_parameter"].sudo()

        # Gdrive picker
        client_id = env.get_param("gdrive_client_id")
        scope = env.get_param(
            "gdrive_scope"
        )  # ['https://www.googleapis.com/auth/drive']
        mimetypes = env.get_param(
            "gdrive_mimetypes"
        )  # "image/png,image/jpeg,image/jpg"
        navbar_hidden = env.get_param(
            "gdrive_navbar_hidden"
        )  #'google.picker.Feature.NAV_HIDDEN'
        locale = env.get_param("gdrive_locale")  # setLocale('en').
        dir = env.get_param(
            "gdrive_dir"
        )  # addView(new google.picker.DocsUploadView().setParent(dir))
        gdrive_storage = env.get_param("gdrive_storage")
        gdrive_options = {
            "client_id": client_id,
            "scope": scope,
            "mimetypes": mimetypes,
            "navbar_hidden": navbar_hidden,
            "locale": locale,
            "dir": dir,
            "gdrive_storage": gdrive_storage,
        }
        result.update({"gdrive": gdrive_options})

        return result
