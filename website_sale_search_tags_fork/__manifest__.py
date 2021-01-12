# -*- coding: utf-8 -*-
# Copyright (C) 2020 Shurshilov Artem <shurshilov.a@yandex.ru>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': "Website Search Product Tags",

    'summary': """
        Search website products by tags such as categories good and complete search""",

    'author': "Shurshilov Artem",
    'website': "http://www.eurodoo.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'eCommerce',
    'version': '13.0.0.0',
    "license": 'LGPL-3',
    'price': 29,
    'currency': 'EUR',
    'images': [
        'static/description/search.png',
        'static/description/product_tags.png',
        'static/description/web_search_tags.png',
    ],

    # any module necessary for this one to work correctly
    'depends': ['website_sale', 'product_tags_fork', 'stock'],
    'installable': True,

    # always loaded
    # 'data': [
    #     'views/views.xml',
    # ],

    # 'qweb': [
    #     "static/src/xml/base.xml",
    # ],
}
