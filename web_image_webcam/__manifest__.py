# -*- coding: utf-8 -*-
# Copyright 2019-2022 Shurshilov Artem <shurshilov.a@yandex.ru>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    "name": "Web Widget - Image WebCam",
    "summary": """Allows to take image with WebCam
    [TAGS] web camera web foto web photo web images camera 
    image snapshot web snapshot webcam snapshot picture web contact
    image web product image online mobile web image produt mobile""",
    "version": "15.1.1.0",
    "category": "web",
    "website": "https://www.eurodoo.com",
    "author": "Shurshilov Artem",
    "license": "LGPL-3",
    "price": 19.00,
    'images': [
            'static/description/field.png',
            'static/description/choose.png',
    ],
    "currency": "EUR",
    "depends": [
        "web",
    ],

    'assets': {
        'web.assets_backend': [
            'web_image_webcam/static/src/**/*.css',
            'web_image_webcam/static/src/js/webcam_widget_new.js',
        ],
        'web.assets_qweb': [
            'web_image_webcam/static/src/xml/web_widget_image_webcam.xml',
        ],
    },
    "installable": True,
}
