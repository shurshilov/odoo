# -*- coding: utf-8 -*-
# Copyright (C) 2020 Artem Shurshilov <shurshilov.a@yandex.ru>
# License OPL-1.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': "POS Cashier Select",

    'summary': """
        Select user selection when click on payment""",

    'author': "Shurshilov Artem",
    'website': "https://eurodoo.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Technical Settings',
    'version': '13.0.0.0',
    "license": "LGPL-3",
    #'price': 9,
    #'currency': 'EUR',
    'images':[
        'static/description/result.png',
        'static/description/click.png',
        'static/description/click.png',
        'static/description/youtube.png',
    ],

    # any module necessary for this one to work correctly
    'depends': ['base','point_of_sale'],
    'installable': True,

    # always loaded
    'data': [
        'views.xml',
    ],

}
