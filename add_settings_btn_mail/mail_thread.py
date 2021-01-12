# -*- coding: utf-8 -*-
#
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2017-2018 Shurshilov Artem <shurshilov.a@yandex.ru>
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
from odoo import api, fields, models

class MailThread(models.AbstractModel):
    _name = 'mail.thread'
    #_inherit = ['mail.thread', 'ir.needaction_mixin']
    _inherit = ['mail.thread']

    hide_notification = fields.Boolean('Hide notification', help="If checked filter messages by not notification.", auto_join=True,)