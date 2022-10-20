# -*- coding: utf-8 -*-
# Copyright (C) 2020-2021 Artem Shurshilov <shurshilov.a@yandex.ru>
# License OPL-1.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': "Android FREE push notificator",

    'summary': """
        Provide free unlimited push notifications on android phones, absolutely free,
        which free android App (used Firebase Push Notifications) work even App close""",

    'author': "Shurshilov Artem",
    'website': "https://eurodoo.com",
    "live_test_url": "https://eurodoo.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Mail',
    'version': '15.2.0.4',
    "license": "OPL-1",
    'images': [
        'static/description/and.png',
    ],

    # any module necessary for this one to work correctly
    'depends': ['base', 'web', 'mail'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/res_users.xml',
        'views/res_config_settings_views.xml',
    ],
}
