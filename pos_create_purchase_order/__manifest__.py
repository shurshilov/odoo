# Copyright (C) 2021 Artem Shurshilov <shurshilov.a@yandex.ru>
# License OPL-1.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "POS create purchase order",
    "summary": """Pos create purchase order quick create sales order in POS point of sale""",
    "author": "Shurshilov Artem",
    "website": "https://eurodoo.com",
    "live_test_url": "https://youtu.be/h1fH0Bh_J0c",
    # Categories can be used to filter modules in modules listing
    "category": "Point of sale",
    "version": "0.0.0",
    # any module necessary for this one to work correctly
    "depends": ["web", "point_of_sale", "purchase"],
    "license": "OPL-1",
    "price": 20,
    "currency": "EUR",
    "images": [
        "static/description/preview.gif",
    ],
    "data": [
        "views/pos.xml",
    ],
    "qweb": [
        "static/src/xml/pos.xml",
    ],
    "installable": True,
    "application": False,
    # If it's True, the modules will be auto-installed when all dependencies
    # are installed
    "auto_install": False,
}
