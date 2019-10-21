# -*- coding: utf-8 -*-

from odoo import models, fields, api


class pos_config(models.Model):
    _inherit = "pos.config"

    iface_load_done_order = fields.Boolean(
        string='Allows to load already done orders',
        default=True,
        help='Allows to load already done orders in the frontend to operate '
             'over them, allowing reprint the tickets, return items, etc.',
    )
    iface_load_done_order_max_qty = fields.Integer(
        string='Maximum number of orders to load on the PoS',
        default=10,
        required=True,
        help='Maximum number of orders to load on the PoS at its init. '
             'Set it to 0 to load none (it\'s still posible to load them by '
             'ticket code).',
    )
