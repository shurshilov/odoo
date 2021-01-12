# -*- coding: utf-8 -*-
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2018 Shurshilov Artem <shurshilov.a@yandex.ru>
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