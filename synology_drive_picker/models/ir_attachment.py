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

import base64
import os
import platform
from urllib import parse

from odoo import api, models
from odoo.exceptions import UserError

from .synology_api import filestation


class IrAttachment(models.Model):
    _inherit = "ir.attachment"

    # type = fields.Selection(selection_add=[('synology', 'Synology Drive Cloud')])

    @api.model
    def synology_download(self, path):
        cp = self.env["res.users"].browse(self._uid)
        if (
            not cp.synology_ip
            or not cp.synology_port
            or not cp.synology_user
            or not cp.synology_pass
        ):
            UserError("Please check user synology settings")

        fl = filestation.FileStation(
            cp.synology_ip,
            cp.synology_port,
            cp.synology_user,
            cp.synology_pass,
            cp.synology_https,
        )
        api_name = "SYNO.FileStation.Download"
        info = fl.file_station_list[api_name]
        api_path = info["path"]
        # path_file = "./" +os.path.basename(path)
        url = (
            "%s%s" % (fl.base_url, api_path)
        ) + "?api=%s&version=%s&method=download&path=%s&mode=%s&_sid=%s" % (
            api_name,
            info["maxVersion"],
            parse.quote_plus(path),
            "download",
            fl._sid,
        )
        return url

    @api.model
    def synology_import(self, path, res_model, res_id):
        cp = self.env["res.users"].browse(self._uid)
        if (
            not cp.synology_ip
            or not cp.synology_port
            or not cp.synology_user
            or not cp.synology_pass
        ):
            UserError("Please check user synology settings")

        if cp.synology_storage == "copy":
            fl = filestation.FileStation(
                cp.synology_ip,
                cp.synology_port,
                cp.synology_user,
                cp.synology_pass,
                cp.synology_https,
            )
            # Download to file
            fl.get_file(path, "open")

            # Create attahchment from file
            if platform.system() == "Windows":
                path_file = "./" + os.path.basename(path)
            # else:
            #     path_file = "../" + os.path.basename(path)
            attachment_obj = self.env["ir.attachment"]
            attachment = {
                "name": path.split("/")[-1],
                "type": "binary",
                "datas": base64.b64encode(open(path_file, "rb").read())
                if path_file
                else False,
                "res_id": res_id,
                "res_model": res_model,
                "description": "synology",
            }
            attachment_obj.create(attachment)
        else:
            # Create attahchment from url
            fl = filestation.FileStation(
                cp.synology_ip,
                cp.synology_port,
                cp.synology_user,
                cp.synology_pass,
                cp.synology_https,
            )
            api_name = "SYNO.FileStation.Download"
            info = fl.file_station_list[api_name]
            api_path = info["path"]
            url = (
                "%s%s" % (fl.base_url, api_path)
            ) + "?api=%s&version=%s&method=download&path=%s&mode=%s&_sid=%s" % (
                api_name,
                info["maxVersion"],
                parse.quote_plus(path),
                "open",
                "",
            )  # fl._sid)

            attachment_obj = self.env["ir.attachment"]
            attachment = {
                "name": path.split("/")[-1],
                "type": "url",
                "url": url,
                "res_id": res_id,
                "res_model": res_model,
                "description": "synology",
            }
            attachment_obj.create(attachment)

    @api.model
    def synology(self, funcAPI="get_info", params_list=False):
        # Initiate the classes DownloadStation & FileStation with (ip_address, port, username, password)
        # it will login automatically
        cp = self.env["res.users"].browse(self._uid)
        if (
            not cp.synology_ip
            or not cp.synology_port
            or not cp.synology_user
            or not cp.synology_pass
        ):
            UserError("Please check user synology settings")
        fl = filestation.FileStation(
            cp.synology_ip,
            cp.synology_port,
            cp.synology_user,
            cp.synology_pass,
            cp.synology_https,
        )
        # get_file(self, path=None, mode=None, dest_path=".", chunkSize=8192):
        method_to_call = getattr(fl, funcAPI)
        if params_list:
            return method_to_call(*params_list)
        else:
            return method_to_call()
