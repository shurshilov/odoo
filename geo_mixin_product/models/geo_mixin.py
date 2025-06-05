from odoo import models


class ProductProduct(models.Model):
    _name = "product.template"
    _inherit = ["product.template", "geo.mixin"]
