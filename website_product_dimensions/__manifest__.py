# -*- coding: utf-8 -*-
# Copyright 2018 Artem Shurshilov
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    'name': "Website product dimensions",  # It must be non-technical name of the module
    'summary': """Provide product dimensions in stock and e-commerce for products and display it on website""",  # describe here which problems solved by module
    'author': "Shurshilov Artem",
    'support': "shurshilov.a@yandex.ru",
    'website': "https://vk.com/id20132180",
    "license": "LGPL-3",
    'category': 'Website',
    'version': '12.0.0.0',  # odoo.x.y.z; z - bags, y - feautures, x - model or view big changes
    'images': [
        'static/description/screen.png',
        'static/description/screen1.png',
    ],
    "price": 39.00,
    "currency": "EUR",
    'depends': ['product', ],  # any odoo module necessary for this one to work correctly
    'data':  [  # always loaded
        'views/views.xml',
        'views/templates.xml'
    ],
    'demo': [  # only loaded in demonstration mode
        # 'demo/demo.xml',
    ],
    'qweb': [
        # 'static/src/xml/*.xml'
    ],
    'application': True,
    "auto_install": False,
    "installable": True,
    "sequence": 1,
}
