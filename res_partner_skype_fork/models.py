from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    skype = fields.Char("Skype", index=True)
