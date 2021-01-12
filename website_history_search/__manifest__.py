# -*- coding: utf-8 -*-
# Copyright (C) 2020 Shurshilov Artem <shurshilov.a@yandex.ru>
# License OPL-1.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Website search history',
    'summary': """website search history manage web site cookies""",
    'author': 'Shurshilov Artem',
    "website": "www.eurodoo.com",

    # Categories can be used to filter modules in modules listing
    'category': "eCommerce",
    'version': '13.0.0.0',
    # any module necessary for this one to work correctly
    'depends': ['web', 'website_sale'],
    "license": "LGPL-3",
    'price': 19,
    'currency': 'EUR',
    'images': [
        'static/description/result.png',
        'static/description/result.png',
        'static/description/result.png',
    ],
    'data': [
        'views/template.xml',
    ],
    # 'qweb': [ 'static/src/xml/image.xml', ],
    'installable': True,
    'application': False,
    # If it's True, the modules will be auto-installed when all dependencies
    # are installed
    'auto_install': False,
}
