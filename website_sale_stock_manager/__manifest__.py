# Copyright 2020-2022 Artem Shurshilov <shurshilov.a@yandex.ru>
{
    "name": "website stock manager",
    "summary": """
    Display Product stock on website product page. Qty (quantity) and available ticket.
    Sale only available products on Website stock available quantity website""",
    "version": "14.0.3.0.0",
    "author": "EURO ODOO, Shurshilov Artem",
    "license": "OPL-1",  # MIT
    "category": "eCommerce",
    "support": "shurshilov.a@yandex.ru",
    "website": "https://eurodoo.com",
    "images": [
        "static/description/info.png",
        "static/description/info1.png",
        "static/description/info2.png",
    ],
    "price": 19.00,
    "currency": "EUR",
    "depends": ["website_sale", "stock"],
    "data": [
        "views/website_sale_available_views.xml",
        "views/res_config_settings_views.xml",
    ],
    "installable": True,
}
