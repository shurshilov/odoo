# Copyright 2019-2022 Shurshilov Artem
# License OPL-1.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    "name": "Adds watermark on image product in website",  # It must be non-technical name of the module
    "summary": """
        The module adds watermark on image of product in website.
        In backend-side image of product dont change.
        Tehnical module add new field binary in database with
        copy image + watermark.
        Setting insert in website settings.
        product watermark
        template watermark
        product security
    """,  # describe here which problems solved by module
    "author": "Shurshilov Artem",
    "support": "shurshilov.a@yandex.ru",
    "website": "http://www.eurodoo.com",
    #    'website': "https://vk.com/id20132180",
    "license": "OPL-1",
    "category": "Website",
    "version": "0.0.1",  # odoo.x.y.z; z - bags, y - feautures, x - model or view big changes
    "depends": [
        "base",
        "web",
        "product",
        "website_sale",
    ],  # any odoo module necessary for this one to work correctly
    "data": [  # always loaded
        "views/website.xml",
    ],
    "images": [
        "static/description/screen.png",
        "static/description/screen1.png",
    ],
    "price": 19.00,
    "currency": "EUR",
    "installable": True,
    "application": False,
    "auto_install": False,
}
