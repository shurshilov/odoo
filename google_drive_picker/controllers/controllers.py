import requests
import datetime
import logging
import json
from odoo import http
import base64
from odoo.exceptions import Warning

_logger = logging.getLogger(__name__)


class GdrivePicker(http.Controller):
    @http.route("/gdrive_picker_path", auth="user", type="json", cors="*")
    def gdrive_picker_path(self, **kw):
        try:
            env = http.request.env["ir.config_parameter"].sudo()
            GdriveFolderPatternObj = http.request.env[
                "gdrive.folder.pattern"
            ].sudo()
            url = "https://www.googleapis.com/drive/v3/files"
            get_url = "{}?q=mimeType='application/vnd.google-apps.folder' and trashed = false and name='{}'&fields=*".format(
                url, "file_name"
            )
            access_token = kw.get("gdrive").get("oauthToken")
            parent_id = env.get_param("gdrive_dir")
            dir_id = parent_id
            object = (
                http.request.env[kw.get("res_model")]
                .sudo()
                .browse(kw.get("res_id"))
            )
            if object._description:
                folder_name = object._description
            else:
                folder_name = kw.get("res_model")
            folder_id = str(kw.get("res_id")).zfill(7)
            gdrive_folder_pattern = GdriveFolderPatternObj.search(
                [("model_id.model", "=", kw.get("res_model"))], limit=1
            )
            folder_pattern = ""

            def get_attribute(obj, attrlist):
                if not attrlist:
                    return False
                if not isinstance(attrlist, list):
                    attrlist = attrlist.split(".")
                if len(attrlist) == 1:
                    attrs = attrlist[0].split("|")
                    val = getattr(obj, attrs[0])
                    if len(attrs) > 1:
                        if isinstance(val, datetime.date):
                            val = val.strftime(attrs[1])
                        elif attrs[0] == "id" or val.isnumeric():
                            val = str(val).zfill(int(attrs[1]))
                        else:
                            val = getattr(obj, attrlist[0])
                    return val
                else:
                    obj2 = getattr(obj, attrlist[0])
                    return get_attribute(obj2, attrlist[1:])

            try:
                if gdrive_folder_pattern:
                    fields = gdrive_folder_pattern.pattern.split("/")
                    for field in fields:
                        folder_pattern += str(get_attribute(object, field))
                        if field != fields[-1:][0]:
                            folder_pattern += "-"
                        print(folder_pattern)
            except Exception as e:
                _logger.info(e)
                folder_pattern = False
            if folder_pattern:
                folder_id = folder_pattern
            headers = {"Authorization": "Bearer " + access_token}
            # get all diles by name model or description model
            # if ot found, create it
            res = requests.get(
                get_url.replace("file_name", folder_name), headers=headers
            )
            if res.status_code == 200:
                response = res.json()
                if not response.get("files"):
                    dir_id = self.create_gdrive_folder(
                        url, headers, folder_name, dir_id
                    )
                else:
                    folder_found = False
                    for folder in response.get("files"):
                        if dir_id in folder.get("parents") and not folder.get(
                            "trashed"
                        ):
                            dir_id = folder.get("id")
                            folder_found = True
                            break
                    if not dir_id and not folder_found:
                        folder_found = True
                        dir_id = response.get("files")[0].get("id")
                    if not folder_found:
                        dir_id = self.create_gdrive_folder(
                            url, headers, folder_name, dir_id
                        )
            # get all files by folder_id
            # if ot found, create it
            res = requests.get(
                get_url.replace("file_name", folder_id), headers=headers
            )
            if res.status_code == 200:
                response = res.json()
                if not response.get("files"):
                    dir_id = self.create_gdrive_folder(
                        url, headers, folder_id, dir_id
                    )
                else:
                    folder_found = False
                    for folder in response.get("files"):
                        if dir_id in folder.get("parents") and not folder.get(
                            "trashed"
                        ):
                            dir_id = folder.get("id")
                            folder_found = True
                            break
                    if not dir_id and not folder_found:
                        folder_found = True
                        dir_id = response.get("files")[0].get("id")
                    if not folder_found:
                        dir_id = self.create_gdrive_folder(
                            url, headers, folder_id, dir_id
                        )
            if dir_id:
                return {"dir_id": dir_id}
            else:
                raise Warning(res.text)
        except Exception as e:
            _logger.info(e)
            return {"dir_id": False}

    def create_gdrive_folder(self, url, headers, folder_name, parent_id):
        headers.update({"Content-Type": "application/json"})
        metadata = {
            "name": folder_name,
            "mimeType": "application/vnd.google-apps.folder",
        }
        if parent_id:
            metadata.update({"parents": [parent_id]})
        res = requests.post(url, headers=headers, data=json.dumps(metadata))
        if res.status_code == 200:
            return res.json().get("id")
        else:
            raise Warning(res.text)

    @http.route("/upload_gdrive_file", auth="user", type="json", cors="*")
    def upload_gdrive_file(self, attachment_id, access_token):
        attachment = http.request.env["ir.attachment"].browse(attachment_id)
        if attachment.res_id and attachment.res_model and access_token:
            # get folder for save/import file
            folder_gdrive = self.gdrive_picker_path(
                **{
                    "res_id": attachment.res_id,
                    "res_model": attachment.res_model,
                    "gdrive": {"oauthToken": access_token},
                }
            )
            if folder_gdrive.get("dir_id", False):
                headers = {"Authorization": "Bearer %s" % (access_token)}
                para = {
                    "name": "%s" % (attachment.name),
                    "parents": ["%s" % (folder_gdrive.get("dir_id", False))],
                }
                files = {
                    "data": (
                        "metadata",
                        json.dumps(para),
                        "application/json; charset=UTF-8",
                    ),
                    "file": base64.b64decode(attachment.datas),
                }
                r = requests.post(
                    "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
                    headers=headers,
                    files=files,
                )

                if r.status_code == 200:
                    attachment.update(
                        {
                            "type": "url",
                            "url": "https://docs.google.com/document/d/%s"
                            % r.json().get("id"),
                            "mimetype": attachment.mimetype,
                            "raw": b"",
                        }
                    )
                    if attachment.store_fname:
                        attachment._file_delete(attachment.store_fname)
                    return True
                else:
                    return False
