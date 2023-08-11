# Copyright 2016 Siddharth Bhalgami <siddharth.bhalgami@techreceptives.com>
# Copyright 2019-2022 EURO ODOO, Shurshilov Artem <shurshilov.a@yandex.ru>
# License OPL-1 or later (http://www.gnu.org/licenses/lgpl).
{
    "name": "Web Widget - Attachment WebCam",
    "summary": "Allows to take image with WebCam to Attachments Chatter on fly snapshot Attachments box web camera foto web photo web camera web",
    "version": "14.0.2.0.0",
    "category": "web",
    "website": "https://eurodoo.com",
    "author": "Tech Receptives, "
    "Odoo Community Association (OCA), "
    "Kaushal Prajapati, "
    "EURO ODOO, Shurshilov Artem",
    "license": "OPL-1",
    "price": 15.00,
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
        # "static/src/xml/web_widget_image_webcam.xml",
        "static/src/components/attachment_webcam/attachment_webcam.xml",
        "static/src/components/attachment_box_custom/attachment_box_custom.xml",
    ],
    "installable": True,
}
