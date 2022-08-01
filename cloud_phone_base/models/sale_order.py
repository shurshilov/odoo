from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = "sale.order"

    call_ids = fields.Many2many(
        related="partner_id.call_ids",
        string="Calls",
        comodel_name="cloud.phone.call",
        # compute="_compute_call_ids",
    )
