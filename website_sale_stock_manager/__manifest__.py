# Copyright 2020 Artem Shurshilov <shurshilov.a@yandex.ru>
{
    "name": "website stock manager",
    "summary": """
    Display Product stock on website product page.
    Sale only available products on Website stock available quantity website""",
    "version": "13.0.2.0.0",
    "author": "Shurshilov Artem",
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
    "data": ["views/website_sale_available_views.xml", "views/res_config_settings_views.xml"],
    "installable": True,
}
