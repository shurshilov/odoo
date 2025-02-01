# Copyright (C) 2020-2021 Artem Shurshilov <shurshilov.a@yandex.ru>
# License OPL-1.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Dropbox Picker upload attachments",
    "summary": """Dropbox Picker upload attachments download file search
        add attachment From Dropbox
        search content search content pdf,image,photo and other attachment dropbox attachment
        attachments dropbox attachments chatter dropbox chatter record dropbox record
        from dropbox to odoo files dropbox files file dropbox file
        attachment dropbox attachments dropbox cloud attachment cloud
        attachments""",
    "author": "EURO ODOO, Shurshilov Artem",
    "maintainer": "EURO ODOO",
    "website": "https://eurodoo.com",
    "live_test_url": "https://eurodoo.com/login_employee?login=demo1&amp;password=demo1",
    # Categories can be used to filter modules in modules listing
    "category": "Extra Tools",
    "version": "14.0.0.0",
    # any module necessary for this one to work correctly
    "depends": ["web", "mail"],
    "license": "OPL-1",
    "price": 25,
    "currency": "EUR",
    "images": [
        "static/description/button.png",
    ],
    "data": [
        "views/assets.xml",
        "views/res_config_settings_views.xml",
    ],
    "qweb": [
        "static/src/xml/*.xml",
    ],
    "installable": True,
    "application": False,
    # If it's True, the modules will be auto-installed when all dependencies
    # are installed
    "auto_install": False,
}
