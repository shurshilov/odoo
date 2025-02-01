# Copyright (C) 2023-today Artem Shurshilov <shurshilov.a@yandex.ru>
# License OPL-1.0.
{
    "name": "Email per user. Individual email work, compatible with cloud solutions.",
    "summary": " \
Now users can work both in their personal (corporate) in the mailbox, \
also in odoo at the same time. The message is sent from the user's mailbox, \
the response also comes to the user's mailbox. The message remains unread \
in the email provider's mailbox and also gets into the odoo history.",
    "author": "EURO ODOO, Shurshilov Artem",
    "website": "https://eurodoo.com",
    "live_test_url": "https://eurodoo.com",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Document Management",
    "version": "16.0.0.0",
    "license": "OPL-1",
    "price": 49.0,
    "currency": "EUR",
    "images": [
        "static/description/preview.png",
    ],
    # any module necessary for this one to work correctly
    "depends": ["base", "web", "mail"],
    # always loaded
    "data": [
        "security/ir.model.access.csv",
        "views/menu.xml",
        "views/ir_mail_server.xml",
        "views/fetchmail_server.xml",
        "data/ir_mail_popular.xml",
    ],
}
