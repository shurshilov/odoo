# Copyright (C) 2018-2020 Aurel Balanay - Evanscor Technology Solutions Inc
# Copyright (C) 2020 Artem Shurshilov <shurshilov.a@yandex.ru>
# License LGPL-3 or later (http://www.gnu.org/licenses/agpl).


import logging

import odoo
import pytz
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from odoo import _, api, fields, http, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

# from ftplib import FTP
try:
    import ftplib
except ImportError:
    print("There was no such module named -ftplib- installed")
import datetime
import io
import json
import os
import shutil
import tempfile


class DbBackup(models.Model):
    _name = "db.backup"
    _description = "Backup configuration record"

    # @api.multi
    def get_db_list(self, host, port, context={}):
        return http.db_list(force=True)

    # @api.multi
    def _get_db_name(self):
        return self._cr.dbname

    # Columns for local server configuration
    host = fields.Char("Host", required=True, default="localhost")
    port = fields.Char("Port", required=True, default=8069)
    name = fields.Char(
        "Database",
        required=True,
        help="Database you want to schedule backups for",
        default=_get_db_name,
    )
    folder = fields.Char(
        "Backup Directory",
        help="Absolute path for storing the backups",
        required="True",
        default="/odoo/backups",
    )
    backup_type = fields.Selection(
        [("zip", "Zip"), ("dump", "Dump")],
        "Backup Type",
        required=True,
        default="zip",
    )
    autoremove = fields.Boolean(
        "Auto. Remove Backups",
        help="If you check this option you can choose to automaticly remove the backup after xx days",
    )
    days_to_keep = fields.Integer(
        "Remove after x days",
        help="Choose after how many days the backup should be deleted. For example:\nIf you fill in 5 the backups will be removed after 5 days.",
        required=True,
    )

    # Columns fro Google Drive
    is_upload = fields.Boolean(
        "Upload to Google Drive",
        help="If you check this option you can specify the details needed to upload to google drive.",
    )
    drive_folder_id = fields.Char(
        string="Folder ID",
        help="make a folder on drive in which you want to upload files; then open that folder; the last thing in present url will be folder id",
    )
    gdrive_email_notif_ids = fields.Many2many(
        "res.users", string="Person to Notify"
    )
    drive_autoremove = fields.Boolean(
        "Auto. Remove Uploaded Backups",
        help="If you check this option you can choose to automaticly remove the backup after xx days",
    )

    drive_to_remove = fields.Integer(
        "Remove after x days",
        help="Choose after how many days the backup should be deleted. For example:\nIf you fill in 5 the backups will be removed after 5 days.",
    )

    is_upload_ftp = fields.Boolean(
        "Upload to FTP",
        help="If you check this option you can specify the details needed to upload to FTP server.",
    )
    ftp_folder_id = fields.Char(
        string="FTP Folder path",
        help="make a folder on FTP in which you want to upload files",
    )
    ftp_email_notif_ids = fields.Many2many(
        "res.users",
        "ftp_user_rel",
        "ftp_id",
        "user_id",
        string="Person to Notify",
    )
    ftp_address = fields.Char(string="FTP server ip address")
    ftp_port = fields.Char(string="FTP server port")
    ftp_login = fields.Char(string="FTP server login/username")
    ftp_password = fields.Char(string="FTP server password")
    ftp_autoremove = fields.Boolean(
        "Auto. Remove Uploaded Backups",
        help="If you check this option you can choose to automaticly remove the backup after xx days",
    )

    ftp_to_remove = fields.Integer(
        "Remove after x days",
        help="Choose after how many days the backup should be deleted. For example:\nIf you fill in 5 the backups will be removed after 5 days.",
    )

    @api.constrains("days_to_keep")
    def _check_days_to_keep(self):
        for rec in self:
            if not rec.days_to_keep < 1:
                raise ValidationError(
                    _("Error! days_to_keep should be more than zero.")
                )
        return True

    # @api.depends("google_drive_authorization_code")
    # def _compute_drive_uri(self):
    #     google_drive_uri = self.env["google.service"]._get_google_token_uri(
    #         "drive", scope=self.env["google.drive.config"].get_google_scope()
    #     )
    #     for config in self:
    #         config.google_drive_uri = google_drive_uri

    # def set_values(self):
    #     params = self.env["ir.config_parameter"].sudo()
    #     authorization_code_before = params.get_param("google_drive_authorization_code")
    #     super(DbBackup, self).set_values()
    #     authorization_code = self.google_drive_authorization_code
    #     refresh_token = False
    #     if authorization_code and authorization_code != authorization_code_before:
    #         refresh_token = self.env["google.service"].generate_refresh_token(
    #             "drive", authorization_code
    #         )
    #     params.set_param("google_drive_refresh_token", refresh_token)

    # @api.multi
    def _check_db_exist(self):
        self.ensure_one()

        db_list = self.get_db_list(self.host, self.port)
        if self.name in db_list:
            return True
        return False

    # @api.multi
    def _check_google_drive_authorization_code(self):
        self.ensure_one()
        # params = self.env["ir.config_parameter"].sudo()
        # authorization_code_before = params.get_param("google_drive_authorization_code")
        access_token = (
            self.env["res.config.settings"].sudo().get_access_token_gdrive()
        )
        if access_token:
            return True
        return False

    _constraints = [
        (_check_db_exist, _("Error ! No such database exists!"), []),
        (
            _check_google_drive_authorization_code,
            _(
                "Error ! No set google_drive_authorization_code! Setting it before!"
            ),
            [],
        ),
    ]

    def dump_db_manifest(self, cr):
        pg_version = "%d.%d" % divmod(
            cr._obj.connection.server_version / 100, 100
        )
        cr.execute(
            "SELECT name, latest_version FROM ir_module_module WHERE state = 'installed'"
        )
        modules = dict(cr.fetchall())
        manifest = {
            "odoo_dump": "1",
            "db_name": cr.dbname,
            "version": odoo.release.version,
            "version_info": odoo.release.version_info,
            "major_version": odoo.release.major_version,
            "pg_version": pg_version,
            "modules": modules,
        }
        return manifest

    def dump_db(self, db_name, stream, backup_format="zip"):
        """Dump database `db` into file-like object `stream` if stream is None
        return a file object with the dump"""
        # cron_user_id = self.env.ref('auto_backup.backup_scheduler').user_id.id
        # if self._name != 'db.backup' or cron_user_id != self.env.user.id:
        #     _logger.error('Unauthorized database operation. Backups should only be available from the cron job.')
        #     raise AccessDenied()
        _logger.info("DUMP DB: %s format %s", db_name, backup_format)

        cmd = ["pg_dump", "--no-owner"]
        cmd.append(db_name)

        if backup_format == "zip":
            with tempfile.TemporaryDirectory() as dump_dir:
                filestore = odoo.tools.config.filestore(db_name)
                if os.path.exists(filestore):
                    shutil.copytree(
                        filestore, os.path.join(dump_dir, "filestore")
                    )
                with open(os.path.join(dump_dir, "manifest.json"), "w") as fh:
                    db = odoo.sql_db.db_connect(db_name)
                    with db.cursor() as cr:
                        json.dump(self.dump_db_manifest(self._cr), fh, indent=4)
                cmd.insert(-1, "--file=" + os.path.join(dump_dir, "dump.sql"))
                odoo.tools.exec_pg_command(*cmd)
                if stream:
                    odoo.tools.osutil.zip_dir(
                        dump_dir,
                        stream,
                        include_dir=False,
                        fnct_sort=lambda file_name: file_name != "dump.sql",
                    )
                else:
                    t = tempfile.TemporaryFile()
                    odoo.tools.osutil.zip_dir(
                        dump_dir,
                        t,
                        include_dir=False,
                        fnct_sort=lambda file_name: file_name != "dump.sql",
                    )
                    t.seek(0)
                    return t
        else:
            cmd.insert(-1, "--format=c")
            stdin, stdout = odoo.tools.exec_pg_command_pipe(*cmd)
            if stream:
                shutil.copyfileobj(stdout, stream)
            else:
                return stdout

    @api.model
    def schedule_backup(self):
        conf_ids = self.search([])

        for rec in conf_ids:
            # db_list = self.get_db_list(rec.host, rec.port)

            if rec.name:
                try:
                    if not os.path.isdir(rec.folder):
                        os.makedirs(rec.folder)
                except:
                    raise
                # Create name for dumpfile.
                user_tz = pytz.timezone(
                    self.env.context.get("tz") or self.env.user.tz or "UTC"
                )
                date_today = pytz.utc.localize(
                    datetime.datetime.today()
                ).astimezone(user_tz)
                bkp_file = "%s_%s.%s" % (
                    rec.name,
                    date_today.strftime("%Y-%m-%d_%H_%M_%S"),
                    rec.backup_type,
                )

                file_path = os.path.join(rec.folder, bkp_file)
                # uri = 'http://' + rec.host + ':' + rec.port
                # conn = xmlrpclib.ServerProxy(uri + '/xmlrpc/db')
                try:
                    # try to backup database and write it away
                    print(file_path)
                    fp = open(file_path, "wb")
                    # odoo.service.db.dump_db(rec.name, fp, rec.backup_type)
                    self.dump_db(rec.name, fp, rec.backup_type)
                    fp.close()
                except Exception as error:
                    _logger.debug(
                        "Couldn't backup database %s. Bad database administrator password for server running at http://%s:%s"
                        % (rec.name, rec.host, rec.port)
                    )
                    _logger.debug(
                        "Exact error from the exception: " + str(error)
                    )
                    print("Exact error from the exception: " + str(error))
                    print(
                        "Couldn't backup database %s. Bad database administrator password for server running at http://%s:%s"
                        % (rec.name, rec.host, rec.port)
                    )
                    continue

            else:
                _logger.debug(
                    "database %s doesn't exist on http://%s:%s"
                    % (rec.name, rec.host, rec.port)
                )

            """
            Remove all old files (on local server) in case this is configured..
            """
            if rec.autoremove:
                dir = rec.folder
                # Loop over all files in the directory.
                for f in os.listdir(dir):
                    fullpath = os.path.join(dir, f)
                    # Only delete the ones wich are from the current database
                    # (Makes it possible to save different databases in the same folder)
                    if rec.name in fullpath:
                        timestamp = os.stat(fullpath).st_ctime
                        createtime = datetime.datetime.fromtimestamp(timestamp)
                        now = datetime.datetime.now()
                        delta = now - createtime
                        if delta.days >= rec.days_to_keep:
                            # Only delete files (which are .dump and .zip), no directories.
                            if os.path.isfile(fullpath) and (
                                ".dump" in f or ".zip" in f
                            ):
                                _logger.info(
                                    "Delete local out-of-date file: " + fullpath
                                )
                                os.remove(fullpath)

            self.google_drive_upload(rec, file_path, bkp_file)
            self.ftp_upload(rec, file_path, bkp_file)

    def ftp_upload(self, rec, file_path, bkp_file):
        # FTP UPLOAP
        if rec.is_upload_ftp:
            filename = bkp_file
            ftp = ftplib.FTP(timeout=300)
            ftp.connect(rec.ftp_address, rec.ftp_port)
            ftp.login(rec.ftp_login, rec.ftp_password)
            ftp.encoding = "utf-8"
            ftp.cwd(rec.ftp_folder_id)

            with open(file_path, "rb") as file:
                backup = file.read()
                buf = io.BytesIO(backup)
                buf.seek(0)
                ftp.storbinary("STOR " + filename, buf)

                if len(rec.ftp_email_notif_ids):
                    email_to = ""
                    for record in rec.ftp_email_notif_ids.mapped("login"):
                        email_to += record + ","

                    notification_template = (
                        self.env["ir.model.data"]
                        .sudo()
                        .get_object(
                            "auto_backup_pro", "email_google_drive_upload"
                        )
                    )
                    # ADD fields requered
                    values = notification_template.generate_email(
                        self.id,
                        ["subject", "body_html", "email_from", "email_to"],
                    )
                    values["email_from"] = (
                        self.env["res.users"]
                        .browse(self.env.uid)
                        .company_id.email
                    )
                    values["email_to"] = email_to
                    values["subject"] = "FTP Upload Successful"
                    values["body_html"] = (
                        "<h3>Backup Successfully Uploaded!</h3>"
                        "Please see below details. <br/> <br/> "
                        "<b>Backup File: %s" % (str(bkp_file))
                    )
                    #   " <a href='https://drive.google.com/drive/u/0/folders/%s'>Open</a></b>" % (
                    #       str(rec.drive_folder_id))

                    send_mail = self.env["mail.mail"].create(values)
                    send_mail.send(True)

        # AUTO REMOVE UPLOADED FILE
        if rec.ftp_autoremove:
            pass
            # for file_data in ftp.mlsd():
            #     file_name, meta = file_data
            #     create_date = self.get_datetime_format(meta.get("modify"))
            #     date_today1 = datetime.datetime.today().date()
            #     delta1 = date_today1 - create_date
            #     if delta1.days >= rec.backup_id.days_to_keep:
            #         if file_name.endswith(".zip") or file_name.endswith(".dump"):
            #             if self.env.cr.dbname in file_name:
            #                 ftp.delete(file_name)
            #             if file_name.endswith(".zip") and rec.backup == 'db_and_files':
            #                 fpath = rec.files_path.split('/')[-1]
            #                 if fpath in file_name:
            #                     ftp.delete(file_name)
            #             _logger.info("Delete FTP out-of-date file.")

    def google_drive_upload(self, rec, file_path, bkp_file):
        if rec.is_upload:
            self.env["res.config.settings"].get_access_token_gdrive()
            credentials = self.env[
                "res.config.settings"
            ].get_credentials_gdrive()
            # create drive api client
            service = build("drive", "v3", credentials=credentials)
            file_metadata = {
                "name": "%s" % (str(bkp_file)),
                "parents": ["%s" % (str(rec.drive_folder_id))],
            }
            media = MediaFileUpload(file_path, mimetype="application/json")
            # pylint: disable=maybe-no-member
            file = (
                service.files()
                .create(body=file_metadata, media_body=media, fields="id")
                .execute()
            )
            # g_drive = self.env['google.drive.config']
            # access_token = GoogleDrive.get_access_token(g_drive)
            # GOOGLE DRIVE UPLOAP
            # if rec.is_upload:
            # headers = {"Authorization": "Bearer %s" % (access_token)}
            # para = {
            #     "name": "%s" % (str(bkp_file)),
            #     "parents": ["%s" % (str(rec.drive_folder_id))]
            # }
            # files = {
            #     'data': ('metadata', json.dumps(para), 'application/json; charset=UTF-8'),
            #     'file': open("%s" % (str(file_path)), "rb")
            # }
            # r = requests.post(
            #     "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
            #     headers=headers,
            #     files=files
            # )

            # SENDING EMAIL NOTIFICATION
            if file and len(rec.gdrive_email_notif_ids):
                email_to = ""
                for record in rec.gdrive_email_notif_ids.mapped("login"):
                    email_to += record + ","

                notification_template = (
                    self.env["ir.model.data"]
                    .sudo()
                    .get_object("auto_backup_pro", "email_google_drive_upload")
                )
                # ADD fields requered
                values = notification_template.generate_email(
                    self.id, ["subject", "body_html", "email_from", "email_to"]
                )
                values["email_from"] = (
                    self.env["res.users"].browse(self.env.uid).company_id.email
                )
                values["email_to"] = email_to
                values["subject"] = "Google Drive Upload Successful"
                values["body_html"] = (
                    "<h3>Backup Successfully Uploaded!</h3>"
                    "Please see below details. <br/> <br/> "
                    "<b>Backup File: %s" % (str(bkp_file))
                    + " <a href='https://drive.google.com/drive/u/0/folders/%s'>Open</a></b>"
                    % (str(rec.drive_folder_id))
                )

                send_mail = self.env["mail.mail"].create(values)
                send_mail.send(True)
            elif len(rec.gdrive_email_notif_ids):
                response = r.json()
                code = response["error"]["code"]
                message = response["error"]["errors"][0]["message"]
                reason = response["error"]["errors"][0]["reason"]

                email_to = ""
                for rec in rec.gdrive_email_notif_ids.mapped("login"):
                    email_to += rec + ","

                notification_template = (
                    self.env["ir.model.data"]
                    .sudo()
                    .get_object("auto_backup_pro", "email_google_drive_upload")
                )
                values = notification_template.generate_email(
                    self.id, ["subject", "body_html", "email_from", "email_to"]
                )
                values["email_from"] = (
                    self.env["res.users"].browse(self.env.uid).company_id.email
                )
                values["email_to"] = email_to
                values["subject"] = "Google Drive Upload Failed"
                values["body_html"] = (
                    "<h3>Backup Upload Failed!</h3>"
                    "Please see below details. <br/> <br/> "
                    "<table style='width:100%'>"
                    "<tr> "
                    "<th align='left'>Backup</th>"
                    "<td>" + (str(bkp_file)) + "</td></tr>"
                    "<tr> "
                    "<th align='left'>Code</th>"
                    "<td>" + str(code) + "</td>"
                    "</tr>"
                    "<tr>"
                    "<th align='left'>Message</th>"
                    "<td>" + str(message) + "</td>"
                    "</tr>"
                    "<tr>"
                    "<th align='left'>Reason</th>"
                    "<td>" + str(reason) + "</td>"
                    "</tr> "
                    "</table>"
                )

                send_mail = self.env["mail.mail"].create(values)
                send_mail.send(True)

        # AUTO REMOVE UPLOADED FILE
        # if rec.drive_autoremove:
        #     headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        #     params = {
        #         'access_token': access_token,
        #         'q': "mimeType='application/%s'" % (rec.backup_type),
        #         # 'q': "mimeType='application/zip'",
        #         'fields': "nextPageToken,files(id,name, createdTime, modifiedTime, mimeType)"
        #     }
        #     url = "/drive/v3/files"
        #     status, content, ask_time = self.env['google.service']._do_request(url, params, headers, method='GET')

        #     for item in content['files']:
        #         date_today = datetime.datetime.today().date()
        #         print(str(item['createdTime']))
        #         print(str(item['createdTime'])[0:10])
        #         print(rec.drive_to_remove)
        #         # create_date = datetime.datetime.strptime(str(item['createdTime'])[0:10], '%Y-%m-%d').date()
        #         create_date = fields.Date.from_string(str(item['createdTime'])[0:10])

        #         delta = date_today - create_date
        #         print(delta)
        #         print(item['id'])
        #         if delta.days >= rec.drive_to_remove:
        #             params = {
        #                 'access_token': access_token
        #             }
        #             url = "/drive/v3/files/%s" % (item['id'])
        #             try:
        #                 response = self.env['google.service']._do_request(url, params, headers, method='DELETE')
        #             except requests.HTTPError as e:
        #                 # For some unknown reason Google can also return a 403 response when the event is already cancelled.
        #                 if e.response.status_code != 403:
        #                     raise e
        #                 _logger.info("Could not delete Google event %s" % event_id)
        #             return response
