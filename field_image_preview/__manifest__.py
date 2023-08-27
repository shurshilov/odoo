# Copyright (C) 2016-2023 Shurshilov Artem <shurshilov.a@yandex.ru>
# License LGPL-3
{
    "name": "Widget image preview",
    "summary": """Adds functional preview (open/popup) image in original size
    Enlarge image Enlarge images product images preview product images picture
    foto product photo product preview enlarge """,
    "description": """
This is extension for <field widget="image"> widget image
==============================================
""",
    "author": "Shurshilov Artem",
    #    "website": "https://vk.com/id20132180",
    "website": "http://www.eurodoo.com",
    # Categories can be used to filter modules in modules listing
    "category": "Tools",
    "version": "16.1.0.2",
    # any module necessary for this one to work correctly
    "depends": ["web", "mail"],
    "license": "LGPL-3",
    #    'price': 9.99,
    #    'currency': 'EUR',
    # always loaded
    "images": [
        "static/description/stock_open2.png",
        "static/description/stock_open.png",
        "static/description/stock_cursor.png",
    ],
    "assets": {
        "web.assets_backend": [
            "field_image_preview/static/src/js/image_field.js",
            "field_image_preview/static/src/xml/image.xml",
        ],
    },
    "installable": True,
    "application": False,
    # If it's True, the modules will be auto-installed when all dependencies
    # are installed
    "auto_install": False,
}
