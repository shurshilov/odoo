from odoo import fields, models


class Website(models.Model):
    _inherit = "website"
    _description = "Website"

    webp_enable = fields.Boolean(string="Enable replace images to webp")
    webp_quality = fields.Integer(string="Quality of webp", default=94)
