# Copyright (C) 2020 Artem Shurshilov <shurshilov.a@yandex.ru>
# License OPL-1.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Microsoft Onedrive Picker upload attachments",
    "summary": """Microsoft Onedrive Picker upload attachments download file search""",
    "author": "EURO ODOO, Shurshilov Artem",
    "website": "https://eurodoo.com",
    "live_test_url": "https://eurodoo.com/login_employee?login=demo1&amp;password=demo1",
    # Categories can be used to filter modules in modules listing
    "category": "Extra Tools",
    "version": "14.0.0.2",
    # any module necessary for this one to work correctly
    "depends": ["web", "mail"],
    "license": "OPL-1",
    "price": 19,
    "currency": "EUR",
    "images": [
        "static/description/preview.gif",
    ],
    "data": [
        "views/assets.xml",
        "views/res_config_settings_views.xml",
    ],
    "qweb": [
        "static/src/xml/onedrive.xml",
    ],
    "installable": True,
    "application": False,
    # If it's True, the modules will be auto-installed when all dependencies
    # are installed
    "auto_install": False,
}
