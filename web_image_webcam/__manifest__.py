# -*- coding: utf-8 -*-
# Copyright 2016 Siddharth Bhalgami <siddharth.bhalgami@techreceptives.com>
# Copyright 2019 Shurshilov Artem <shurshilov.a@yandex.ru>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    "name": "Web Widget - Image WebCam",
    "summary": "Allows to take image with WebCam",
    "version": "12.0.1.0.0",
    "category": "web",
    "website": "https://www.eurodoo.com",
    "author": "Tech Receptives, "
              "Odoo Community Association (OCA), "
              "Kaushal Prajapati, "
              "Shurshilov Artem",
    "license": "LGPL-3",
    "price": 19.00,
    "currency": "EUR",
    "data": [
        "views/assets.xml",
    ],
    "depends": [
        "web",
    ],
    "qweb": [
        "static/src/xml/web_widget_image_webcam.xml",
    ],
    "installable": True,
}
