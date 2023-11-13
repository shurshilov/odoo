# Copyright (C) 2020-2023 Artem Shurshilov <shurshilov.a@yandex.ru>
# License OPL-1.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Synology Drive Picker upload attachments",
    "summary": """Synology Drive Picker upload attachments download file search""",
    "author": "EURO ODOO, Shurshilov Artem",
    "website": "https://eurodoo.com",
    "live_test_url": "https://eurodoo.com/login_employee?login=demo1&amp;password=demo777",
    # Categories can be used to filter modules in modules listing
    "category": "Extra Tools",
    "version": "0.3.0",
    # any module necessary for this one to work correctly
    "depends": ["web", "mail"],
    "license": "OPL-1",
    "price": 99,
    "currency": "EUR",
    "images": [
        "static/description/result.png",
    ],
    "data": [
        "views/res_users.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "synology_drive_picker/static/**/*.js",
            "synology_drive_picker/static/src/**/*.xml",
        ],
    },
    "installable": True,
    "application": False,
    # If it's True, the modules will be auto-installed when all dependencies
    # are installed
    "auto_install": False,
}
