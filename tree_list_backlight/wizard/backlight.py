# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (c) 2018 Shurshilov Artem (shurshilov.a@yandex.ru)
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
#
##############################################################################
from odoo import fields, models, api

class Settings(models.TransientModel):
    _name = "backlight.settings"
    _inherit = "res.config.settings"

    models_ids = fields.Many2many('ir.model', string='Models List to work')

    @api.multi
    def set_params(self):
        self.ensure_one()        
        self.env['ir.config_parameter'].set_param("backlight", [rec.model.encode('utf-8') for rec in self.models_ids])