# Copyright 2016 Siddharth Bhalgami <siddharth.bhalgami@techreceptives.com>
# Copyright 2019 Shurshilov Artem <shurshilov.a@yandex.ru>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    "name": "Web Widget - Attachment WebCam",
    "summary": "Allows to take image with WebCam to Attachments Chatter on fly snapshot Attachments box web camera foto web photo web camera web",
    "version": "13.0.2.0.0",
    "category": "web",
    "website": "https://eurodoo.com",
    "author": "Tech Receptives, "
    "Odoo Community Association (OCA), "
    "Kaushal Prajapati, "
    "Shurshilov Artem",
    "license": "LGPL-3",
    "price": 19.00,
    "images": [
        "static/description/field.png",
        "static/description/choose.png",
    ],
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
