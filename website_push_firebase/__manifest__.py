# Copyright (C) 2020 Artem Shurshilov <shurshilov.a@yandex.ru>
# License OPL-1.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Web push marketing. Generate leads from website visitors and send them messages",
    "summary": """Web push marketing. Generate leads from website visitors and send them messages.
     If a visitor gives permission to send him notifications, then regardless of whether his
     computer is turned on or not, he will receive your message (advertising) as soon
     as he turns on the browser.""",
    "author": "EURO ODOO, Shurshilov Artem",
    "website": "https://eurodoo.com",
    "live_test_url": "https://eurodoo.com",
    # Categories can be used to filter modules in modules listing
    "category": "Marketing",
    "version": "14.0.1",
    # any module necessary for this one to work correctly
    "depends": ["web", "crm", "website", "mail_firebase"],
    "license": "OPL-1",
    "price": 29,
    "currency": "EUR",
    "images": [
        "static/description/preview.png",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/assets.xml",
        "views/crm_lead.xml",
        "views/res_config_settings_views.xml",
    ],
    "installable": True,
    "application": False,
    # If it's True, the modules will be auto-installed when all dependencies
    # are installed
    "auto_install": False,
}
