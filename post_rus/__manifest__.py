# Copyright 2018 Artem Shurshilov
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
{
    "name": "Post of Russia integration",
    "summary": "This module allows you to integrate an Odoo with a Russian mail using application",
    "author": "EURO ODOO, Shurshilov Artem",
    "support": "shurshilov.a@yandex.ru",
    "website": "https://eurodoo.com",
    "license": "OPL-1",
    "version": "14.0.0",
    "category": "Sales",
    "sequence": 1,
    "price": 99.00,
    "currency": "EUR",
    "depends": [
        "crm",
        "sale",
        "stock",
        "account",
        "delivery",
    ],
    "data": [
        "security/ir.rule.xml",
        "security/ir.model.access.csv",
        "data/post_rus_data.xml",
        "views/post_delivery.xml",
        "views/post_view.xml",
        "views/post_menu.xml",
        "views/post_setting.xml",
    ],
    "images": [
        "static/description/icon.png",
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
}
