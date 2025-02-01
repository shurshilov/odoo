# Copyright (C) 2020 Artem Shurshilov <shurshilov.a@yandex.ru>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Social manager website 35+ top messangers and social networks svg",
    "summary": """
        Professional social manager
        website 35+ top messangers and social networks svg
        launch application by click
        customize icon features""",
    "author": "Shurshilov Artem",
    "website": "https://eurodoo.com",
    "live_test_url": "https://eurodoo.com",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "eCommerce",
    "version": "13.0.0.0",
    "license": "LGPL-3",
    "support": "shurshilov.a@yandex.ru",
    "price": 19,
    "currency": "EUR",
    "images": [
        "static/description/button.png",
        "static/description/result.png",
        "static/description/result.png",
    ],
    # any module necessary for this one to work correctly
    "depends": ["web", "website", "website_sale"],
    "installable": True,
    # always loaded
    "data": [
        "security/ir.model.access.csv",
        "website_sale_social_networks.xml",
        "data.xml",
    ],
    # 'qweb': [
    #     "static/src/xml/base.xml",
    # ],
}
