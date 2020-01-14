# -*- coding: utf-8 -*-
# Copyright (C) 2019 Artem Shurshilov <shurshilov.a@yandex.ru> WWW.EURODOO.COM
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': "pos_order_list",

    'summary': """
        Adds button my orders in POS interface""",

    'author': "Shurshilov Artem",
    'website': "http://www.eurodoo.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'POS',
    'version': '11.0.0.0',
    "license": "LGPL-3",
    'images':[
     'static/description/stock_open2.png',
        'static/description/stock_cursor.png',
     'static/description/stock_open.png',

    ],

    # any module necessary for this one to work correctly
    'depends': ['base','point_of_sale'],

    # always loaded
    'data': [
        'views/assets_template.xml',
        'views/pos_config.xml',
    ],
    'qweb': [
        'static/src/xml/pos.xml',
    ],

}
