# -*- coding: utf-8 -*-
# Copyright (C) 2020 Artem Shurshilov <shurshilov.a@yandex.ru>
# License OPL-1.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Synology Drive Picker upload attachments",
    "summary": """Synology Drive Picker upload attachments download file search""",
    "author": "EURO ODOO, Shurshilov Artem",
    "website": "https://eurodoo.com",
    "live_test_url": "https://eurodoo.com/login_employee?login=demo1&amp;password=demo1",
    # Categories can be used to filter modules in modules listing
    "category": "Extra Tools",
    "version": "13.2.0.2",
    # any module necessary for this one to work correctly
    "depends": ["web", "mail"],
    "license": "OPL-1",
    "price": 99,
    "currency": "EUR",
    "images": [
        "static/description/result.png",
    ],
    "data": [
        # "views/assets.xml",
        "views/res_users.xml",
    ],
    # "qweb": [
    #     "static/src/xml/synology.xml",
    # ],
    "assets": {
        "web.assets_backend": [
            "google_drive_picker/static/**/*.js",
        ],
        "web.assets_qweb": [
            "google_drive_picker/static/src/**/*.xml",
        ],
    },
    "installable": True,
    "application": False,
    # If it's True, the modules will be auto-installed when all dependencies
    # are installed
    "auto_install": False,
}
