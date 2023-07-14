# Copyright (C) 2021 Artem Shurshilov <shurshilov.a@yandex.ru>
# License OPL-1.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "no auto subscribe, subscribe manager",
    "summary": " \
enable/disable auto subscribe when send message \
no auto subsribe no auto subscription no auto followers \
no auto follower no automatic subscription automatic subsribe\
no auto adds followers no auto follower disciple \
disable adds followers disable add follower disable auto subscribe    \
",
    "author": "EURO ODOO, Shurshilov Artem",
    "website": "https://eurodoo.com",
    "live_test_url": "https://eurodoo.com",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Mail",
    "version": "14.0.0.0",
    "license": "OPL-1",
    "price": 19.0,
    "currency": "EUR",
    "images": [
        "static/description/preview.png",
    ],
    # any module necessary for this one to work correctly
    "depends": ["base", "mail"],
    "sequence": 99,
    # always loaded
    "data": [
        "views/mail_compose_message.xml",
    ],
}
