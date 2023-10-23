# Copyright 2020 Shurshilov Artem
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import base64

from odoo import api, fields, models


class File(models.Model):
    _inherit = "dms.file"

    content = fields.Binary(
        compute="_compute_content",
        inverse="_inverse_content",
        string="Content",
        attachment=False,
        prefetch=False,
        required=False,
        store=False,
    )
    save_type_related = fields.Selection(
        related="directory_id.storage_id.save_type",
        string="Save type",
        readonly=True,
    )
    url_gdrive = fields.Char("Url Gdrive", index=True, size=1024)
    url_onedrive = fields.Char("Url Onedrive", index=True, size=1024)
    url_dropbox = fields.Char("Url Dropbox", index=True, size=1024)

    def _get_share_url(self, redirect=False, signup_partner=False, pid=None):
        self.ensure_one()
        if self.save_type_related == "gdrive":
            return self.url_gdrive

        if self.save_type_related == "onedrive":
            return self.url_onedrive

        if self.save_type_related == "dropbox":
            return self.url_dropbox
        return super()._get_share_url(redirect, signup_partner, pid)

    @api.model
    def create(self, vals):
        storage = self.env["dms.directory"].browse(vals["directory_id"])
        if storage:
            type = storage.storage_id.save_type
            if type in ["gdrive", "onedrive", "dropbox"]:
                vals["content"] = "R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"
        line = super().create(vals)
        return line

    @api.depends("content_binary", "content_file")
    def _compute_content(self):
        bin_size = self.env.context.get("bin_size", False)
        for record in self:
            if record.save_type_related in ["gdrive", "onedrive", "dropbox"]:
                record.content = base64.b64encode(
                    b"R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"
                )
            elif record.content_file:
                context = {"human_size": True} if bin_size else {"base64": True}
                record.content = record.with_context(context).content_file
            else:
                record.content = base64.b64encode(record.content_binary)


class Storage(models.Model):
    _inherit = "dms.storage"

    save_type = fields.Selection(
        selection_add=[
            ("gdrive", "Google Gdrive"),
            ("onedrive", "Microsoft Onedrive"),
            ("dropbox", "Dropbox"),
        ]
    )


class PortalShare(models.TransientModel):
    _inherit = "portal.share"

    @api.model
    def default_get(self, fields):
        result = super().default_get(fields)
        result["res_model"] = self._context.get("active_model", False)
        result["res_id"] = self._context.get("active_id", False)
        if result["res_model"] and result["res_id"]:
            record = self.env[result["res_model"]].browse(result["res_id"])
            result["share_link"] = record.get_base_url() + record._get_share_url(redirect=True)
            if record.save_type_related == "gdrive":
                result["share_link"] = record.url_gdrive

            if record.save_type_related == "onedrive":
                result["share_link"] = record.url_gdrive

            if record.save_type_related == "dropbox":
                result["share_link"] = record.url_gdrive

        return result

    @api.depends("res_model", "res_id")
    def _compute_share_link(self):
        for rec in self:
            rec.share_link = False
            if rec.res_model:
                res_model = self.env[rec.res_model]
                if isinstance(res_model, self.pool["portal.mixin"]) and rec.res_id:
                    record = res_model.browse(rec.res_id)
                    rec.share_link = record.get_base_url() + record._get_share_url(redirect=True)
                    if record.save_type_related == "gdrive":
                        rec.share_link = record.url_gdrive

                    if record.save_type_related == "onedrive":
                        rec.share_link = record.url_gdrive

                    if record.save_type_related == "dropbox":
                        rec.share_link = record.url_gdrive
