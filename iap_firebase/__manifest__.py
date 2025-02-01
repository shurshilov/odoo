# Copyright (C) 2019 Artem Shurshilov <shurshilov.a@yandex.ru>
# License OPL-1.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "IAP Firebase push notifications ODOO mobile apps",
    "summary": """
        Provide free unlimited push mobile notifications and chats on odoo mobile applications (iOS and Android)""",
    "author": "Shurshilov Artem",
    "website": "https://eurodoo.com",
    "live_test_url": "https://eurodoo.com",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Mail",
    "version": "12.0.0.1",
    "license": "OPL-1",
    "price": 299,
    "currency": "EUR",
    "images": [
        "static/description/m6.png",
    ],
    # any module necessary for this one to work correctly
    "depends": ["base", "web", "mail", "iap"],
    # always loaded
    "data": [
        "security/ir.model.access.csv",
        "views/res_users.xml",
        "views/iap_firebase.xml",
    ],
    # 'qweb': [
    #     "static/src/xml/attendance.xml",
    # ],
}
