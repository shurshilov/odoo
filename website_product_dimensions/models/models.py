# -*- coding: utf-8 -*-
# Copyright 2018 Artem Shurshilov
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import models, fields, api, _


class Product(models.Model):
    _inherit = 'product.template'


    display_dimensions = fields.Boolean(string='Display dimensions on website?', default=True)
    length = fields.Float(string='Length',)
    width = fields.Float(string='Width',)
    height = fields.Float(string='Height',)
    volume_auto = fields.Float(string='Volume', compute='_compute_volume_auto',)
    dimensions_uom_id = fields.Many2one(
        'product.uom',
        'Dimension(UOM)',
        domain=lambda self: [('category_id', '=', self.env.ref('product.uom_categ_length').id)],
        help="Default Unit of Measure used for dimension."
    )
    weight_uom_id = fields.Many2one(
        'product.uom',
        'Weight(UOM)',
        domain=lambda self: [('category_id', '=', self.env.ref('product.product_uom_categ_kgm').id)],
        help="Default Unit of Measure used for weight."
    )

    @api.multi
    @api.depends('length', 'width', 'height')
    def _compute_volume_auto(self):
        for rec in self:
            rec.volume_auto = rec.height * rec.width * rec.length
