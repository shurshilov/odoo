# -*- coding: utf-8 -*-
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2018 Artem Shurshilov <shurshilov.a@yandex.ru>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
from openerp import api
from openerp import fields
from openerp import models

class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.depends('tag_ids')
    def _get_tag_search_string(self):
        for rec in self:
            name_search_string = rec.name
            for tag in rec.tag_ids:
                name_search_string += '|' + tag.name
            rec.tag_ids_name = name_search_string
        return name_search_string

    tag_ids_name = fields.Char(compute="_get_tag_search_string",string="Tags name",store="True")

    @api.model
    def create_from_ui_tag(self, id, value):
        tmpl_id = self.search([('product_variant_ids','in',id)])
        if tmpl_id:
            for i in tmpl_id.tag_ids:
                if(i.name == value):
                    return 'Tag alreay exist'
            tag_id = self.env['product.tag'].create({'name':value})
            tmpl_id.tag_ids = [(4,tag_id.id)]
            return 'Tag success create'
        return 'Product template not found'