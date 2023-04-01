# -*- coding: utf-8 -*-
# Copyright 2018 Onestein
# Copyright 2020 Artem Shurshilov
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Speedup Website',
    'summary': """Optimize website odoo core
Speed up your website

""",
    'category': 'Website',
    'version': '14.0.0.0',
    'author': 'EURO ODOO, Shurshilov Artem',
    'license': 'LGPL-3',
    'website': "https://eurodoo.com",
    'price': 49,
    'currency': 'EUR',
    'depends': [
        'website'
    ],
    'images':[
        'static/description/lazy.png',
    ],
    'data': [
        'templates/assets.xml',
    ],
}
