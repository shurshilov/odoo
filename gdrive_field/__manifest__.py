# Copyright (C) 2020 Artem Shurshilov <shurshilov.a@yandex.ru>
# License OPL-1.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Google Drive Picker upload attachments",
    "summary": """Google Drive Picker upload attachments download file search""",
    "author": "Shurshilov Artem",
    "website": "https://eurodoo.com",
    "live_test_url": "https://eurodoo.com/login_employee?login=demo1&amp;password=demo1",
    # Categories can be used to filter modules in modules listing
    "category": "Extra Tools",
    "version": "13.1.0.1",
    # any module necessary for this one to work correctly
    "depends": ["web"],
    "license": "OPL-1",
    "price": 29,
    "currency": "EUR",
    "images": [
        "static/description/result.png",
    ],
    "data": [
        "views/assets.xml",
        "views/res_config_settings_views.xml",
    ],
    "qweb": [
        "static/src/xml/gdrive.xml",
    ],
    "installable": True,
    "application": False,
    # If it's True, the modules will be auto-installed when all dependencies
    # are installed
    "auto_install": False,
}
