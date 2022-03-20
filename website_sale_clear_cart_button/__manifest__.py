# -*- coding: utf-8 -*-
# Copyright (C) 2020 Artem Shurshilov <shurshilov.a@yandex.ru>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': "Clear cart button on website",

    'summary': """
        Clear cart button add on website""",

    'author': "Shurshilov Artem",
    'website': "https://eurodoo.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'eCommerce',
    'version': '13.0.0.0',
    "license": "LGPL-3",
    "support": "shurshilov.a@yandex.ru",
    # 'price': 29,
    # 'currency': 'EUR',
    'images':[
        'static/description/button.png',
        'static/description/result.png',
        'static/description/result.png',
    ],

    # any module necessary for this one to work correctly
    'depends': ['website_sale'],
    'installable': True,

    # always loaded
    'data': [
        'website_sale_clear_cart_button_views.xml',
    ],

    # 'qweb': [
    #     "static/src/xml/base.xml",
    # ],
}
