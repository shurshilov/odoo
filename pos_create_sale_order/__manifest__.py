# Copyright (C) 2021-2022 Artem Shurshilov <shurshilov.a@yandex.ru>
# License OPL-1.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "POS create sale order",
    "summary": """Pos create sale order quick create sales order in POS point of sale""",
    "author": "Shurshilov Artem",
    "website": "https://eurodoo.com",
    "live_test_url": "https://youtu.be/h1fH0Bh_J0c",
    # Categories can be used to filter modules in modules listing
    "category": "Point of sale",
    "version": "0.0.0",
    # any module necessary for this one to work correctly
    "depends": ["web", "point_of_sale"],
    "license": "OPL-1",
    "price": 20,
    "currency": "EUR",
    "images": [
        "static/description/preview.gif",
    ],
    "assets": {
        "point_of_sale.assets": [
            "pos_create_sale_order/static/src/js/pos_create_sales_order.js",
        ],
        "web.assets_qweb": [
            "pos_create_sale_order/static/src/xml/**/*.xml",
        ],
    },
    "installable": True,
    "application": False,
    # If it's True, the modules will be auto-installed when all dependencies
    # are installed
    "auto_install": False,
}
