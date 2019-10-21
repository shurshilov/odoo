# -*- coding: utf-8 -*-
# Copyright 2018 Artem Shurshilov
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
{
    'name': "attachments tools",  # It must be non-technical name of the module
    'summary': """add feautures to sidebar document attachments""",  # describe here which problems solved by module
    'author': "Eyekraft, Shurshilov Artem",
    'support': "shurshilov.a@yandex.ru",
    'website': "http://www.eurodoo.com",
    "license": "LGPL-3",
    'category': 'Document Management',
    'version': '10.1.0.0',  # odoo.x.y.z; z - bags, y - feautures, x - model or view big changes
    'images': [
        'static/description/screen.png',
        'static/description/screen1.png',
        'static/description/screen2.png',
    ],
    'depends': ['base'],  # any odoo module necessary for this one to work correctly
    'data': [  # always loaded
        'views/assets.xml',
    ],
    'demo': [  # only loaded in demonstration mode
        # 'demo/demo.xml',
    ],
    'qweb': [
        'static/src/xml/*.xml'
    ],
    'application': False,
    "auto_install": False,
    "installable": True,
}
# "price": 9.00,
# "currency": "EUR",
# "live_test_url": "http://tcrm.eyekraft.ru/web/action=101",
# "external_dependencies": {"python": [], "bin": []},
# Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
# Accounting • Discuss • Document Management • eCommerce • Human Resources
# Industries • Localization • Manufacturing • Marketing • Point of Sale •
# Productivity • Project • Purchases • Sales • Warehouse • Website • Extra Tools
