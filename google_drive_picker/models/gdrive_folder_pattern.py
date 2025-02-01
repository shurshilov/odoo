from odoo import fields, models, api, _
from odoo.exceptions import UserError


class GdriveFolderPattern(models.Model):
    _name = "gdrive.folder.pattern"

    @api.constrains("model_id")
    def check_model_id(self):
        if len(self.search([("model_id", "=", self.model_id.id)])) > 1:
            raise UserError(_("You cannot assign same object more than once"))

    model_id = fields.Many2one("ir.model", domain=[("transient", "=", False)])
    pattern = fields.Char(
        "Folder Pattern (Please enter fields seperated by '-' if have multiple, i.e. name-id)"
    )
