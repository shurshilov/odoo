# -*- coding: utf-8 -*-
# Copyright 2019 Shurshilov Artem <shurshilov.a@yandex.ru>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    "name": "Website free map, yandex API",
    "summary": """Adds to your website map in contact us form. 
        and allows use yandex API map""",
    "version": "12.0.0.0.0",
    "category": "web",
    "website": "https://www.eurodoo.com",
    "author": "Shurshilov Artem",
    "license": "LGPL-3",
    #"price": 19.00,
    'images':[
            'static/description/field.png',
            'static/description/choose.png',
    ],
    #"currency": "EUR",
    "data": [
        "views/assets.xml",
    ],
    "depends": [
        "web",
    ],
    "qweb": [
        "static/src/xml/website_yandex_map.xml",
    ],
    "installable": True,
}
