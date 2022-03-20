# -*- coding: utf-8 -*-
# Copyright (C) 2021 Artem Shurshilov <shurshilov.a@yandex.ru>
# License OPL-1.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Calendar counter by day',
    'summary': """Calendar counter by date calendar counter calendar count calendar sum calendar""",
    'author': 'Shurshilov Artem, Advance',
    "website": "https://eurodoo.com",
    #"live_test_url": "https://eurodoo.com/login_employee?login=demo1&amp;password=demo1",

    # Categories can be used to filter modules in modules listing
    'category': "Extra Tools",
    'version': '14.0.0.1',
    # any module necessary for this one to work correctly
    'depends': ['web'],
    "license": "LGPL-3",
    # "license": "OPL-1",
    # 'price': 39,
    # 'currency': 'EUR',
    'images': [
        'static/description/yearcal.png',
    ],
    'data': [
        'views/assets.xml',
        # 'views/res_config_settings_views.xml',
    ],
    # 'qweb': ['static/src/xml/*.xml', ],
    'installable': True,
    'application': False,
    # If it's True, the modules will be auto-installed when all dependencies
    # are installed
    'auto_install': False,
}
