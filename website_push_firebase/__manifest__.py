# Copyright (C) 2020 Artem Shurshilov <shurshilov.a@yandex.ru>
# License OPL-1.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Lead from website visitor firebase push notifications",
    "summary": """Lead from website visitor firebase push notifications""",
    "author": "Shurshilov Artem",
    "website": "https://eurodoo.com",
    "live_test_url": "https://eurodoo.com",
    # Categories can be used to filter modules in modules listing
    "category": "Extra Tools",
    "version": "14.0.0.0",
    # any module necessary for this one to work correctly
    "depends": ["web", "crm", "website", "mail_firebase"],
    "license": "OPL-1",
    "price": 29,
    "currency": "EUR",
    "images": [
        "static/description/result.png",
    ],
    "data": [
        # 'security/ir.model.access.csv',
        "views/assets.xml",
        "views/crm_lead.xml",
        "views/res_config_settings_views.xml",
    ],
    #'qweb': ['static/src/xml/onedrive.xml', ],
    "installable": True,
    "application": False,
    # If it's True, the modules will be auto-installed when all dependencies
    # are installed
    "auto_install": False,
}
