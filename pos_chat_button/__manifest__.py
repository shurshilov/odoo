# -*- coding: utf-8 -*-
##############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#    Copyright (C) 2018-Today Shurshilov Artem(shurshilov.a@yandex.ru).
#    Author: Shurshilov Artem
#    you can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    It is forbidden to publish, distribute, sublicense, or sell copies
#    of the Software or modified copies of the Software.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    GENERAL PUBLIC LICENSE (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': "POS Chat (Chatter)",
    'summary': """Chat (chatter) In POS Screen""",
    'description': "This module adds chat interface in Point of sale screen.",
    'license': 'AGPL-3',
    'author': "Shurshilov Artem",
    'website': "http://www.eurodoo.com",
#    'website': "https://vk.com/id20132180",
    'category': 'Point Of Sale',
    'version': '1.0.0',
    'price': 29.00,
    'currency': 'EUR',
    'depends': ['base', 'point_of_sale'],
    'data': ['views/pos_chat.xml'],
    'qweb': ['static/src/xml/pos_msg.xml'],
    'images': [
    'static/description/Odoo POS.png',
    'static/description/Odoo POS1.png',
    'static/description/Odoo POS2.png',
    ],
    'installable': False,
    'auto_install': False,
}
