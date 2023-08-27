from odoo import fields, models


class Users(models.Model):
    _inherit = "res.users"

    print_facsimile = fields.Boolean(related="company_id.print_facsimile")
    facsimile = fields.Binary("Facsimile")
