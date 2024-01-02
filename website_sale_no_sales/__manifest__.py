# Copyright 2018 Denis Mudarisov <https://it-projects.info/team/trojikman>
# Copyright 2019 Kolushov Alexandr <https://it-projects.info/team/KolushovAlexandr>
# Copyright 2020 Artem Shurshilov <shurshilov.a@yandex.ru>
# License MIT (https://opensource.org/licenses/MIT).
{
    "name": "Stop/Allow online sales on website",
    "summary": """Adds options to disable all sales and hide all prices,
     but keep products visible at website
     allow disable sales allow sale website
     site allow disable sales stop online sales allow""",
    "category": "eCommerce",
    "images": [
        "static/description/product_sale.png",
        "static/description/product_no_sale.png",
        "static/description/shop_sale.png",
        "static/description/shop_no_sale.png",
    ],
    "version": "13.0.1",
    "application": False,
    "author": "Shurshilov Artem,IT-Projects LLC, Denis Mudarisov",
    "support": "shurshilov.a@yandex.ru",
    "website": "https://eurodoo.com",
    "license": "Other OSI approved licence",  # MIT
    "price": 10.00,
    "currency": "EUR",
    "depends": ["website_sale"],
    "data": ["templates.xml"],
    "auto_install": False,
    "installable": True,
}
