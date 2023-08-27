from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    inn = fields.Char("INN", size=12)
    kpp = fields.Char("KPP", size=9)
    okpo = fields.Char("OKPO", size=14)
    ogrn = fields.Char(string="ОГРН")
    type = fields.Selection(selection_add=[("director", "Директор")])
