# -*- coding: utf-8 -*-
# Copyright 2019 Shurshilov Artem
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models


class Lead(models.Model):
    _inherit = 'crm.lead'
    attachment = fields.Binary(string='attachment', attachment=True)
