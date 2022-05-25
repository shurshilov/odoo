# -*- coding: utf-8 -*-
# Copyright (C) 2020-2022 Artem Shurshilov <shurshilov.a@yandex.ru>
# License OPL-1.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': "Show/Hide NumPad POS",

    'summary': """
        Show/Hide NumPad POS""",

    'author': "Shurshilov Artem",
    'website': "https://eurodoo.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Point Of Sale',
    'version': '15.0.0.0',
    "license": "LGPL-3",
    # 'price': 29,
    # 'currency': 'EUR',
    'images': [
        'static/description/button.png',
        'static/description/result.png',
        'static/description/result.png',
        'static/description/report_form.png',
    ],

    # any module necessary for this one to work correctly
    'depends': ['base', 'point_of_sale'],
    'installable': True,

    'assets': {
        'web.assets_backend': [
            'hide_show_numpad/static/src/js/hide_numpad.js',
        ],
        'web.assets_qweb': [
            'hide_show_numpad/static/src/**/*.xml',
        ],
    },
    'qweb': [
        'static/src/xml/pos.xml',
    ],
}
