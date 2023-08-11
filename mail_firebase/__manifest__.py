# Copyright (C) 2020 Artem Shurshilov <shurshilov.a@yandex.ru>
# License OPL-1.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Mail message Firebase push notifications",
    "summary": """
        Provide free unlimited push notifications and chats odoo mail messaged (discuss, chat, chatter etc...)""",
    "author": "EURO ODOO, Shurshilov Artem",
    "website": "https://eurodoo.com",
    "live_test_url": "https://eurodoo.com",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Mail",
    "version": "12.0.0.1",
    "license": "OPL-1",
    "price": 19,
    "currency": "EUR",
    "images": [
        "static/description/preview.png",
    ],
    # any module necessary for this one to work correctly
    "depends": ["base", "web", "mail"],
    # always loaded
    "data": [
        "security/ir.model.access.csv",
        "views/assets.xml",
        "views/res_users.xml",
        #'views/iap_firebase.xml',
        "views/res_config_settings_views.xml",
    ],
    # 'qweb': [
    #     "static/src/xml/discuss.xml",
    # ],
}
