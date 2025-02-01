# Copyright (C) 2021-2023 Artem Shurshilov <shurshilov.a@yandex.ru>
# License OPL-1.0 (Odoo Proprietary License v1.0)
{
    "name": "Website webp",
    "summary": """
        website webp website
        speedup website speedup webp speedup
        compress webp compress
        images to webp images webp images
        site webp site
        frontend webp frontend
        webp image webp photo webp photo picture webp picture
        image to webp image speedup webp convert webp convert
        auto convert webp auto quality webp
        """,
    "author": "EURO ODOO, Shurshilov Artem",
    "maintainer": "EURO ODOO",
    "website": "https://eurodoo.com",
    "live_test_url": "https://eurodoo.com/blog",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Website",
    "version": "16.0.0.0.1",
    "license": "OPL-1",
    "support": "shurshilov.a@yandex.ru",
    "price": 39,
    "currency": "EUR",
    "images": [
        "static/description/button.png",
        "static/description/result.png",
        "static/description/result.png",
    ],
    "external_dependencies": {"python": ["webp"]},
    # any module necessary for this one to work correctly
    "depends": ["web", "website"],
    "installable": True,
    # always loaded
    "data": [
        "website.xml",
    ],
}
