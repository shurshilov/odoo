# Copyright 2019-2024 EURO ODOO, Shurshilov Artem <shurshilov.a@yandex.ru>
# License OPL-1 or later
{
    "name": "Web Widget - Attachment WebCam",
    "summary": "Allows to take image with WebCam to Attachments Chatter on fly snapshot Attachments box web camera foto web photo web camera web",
    "version": "16.0.1.0.1",
    "category": "web",
    "website": "https://eurodoo.com",
    "author": "EURO ODOO, Shurshilov Artem",
    "license": "OPL-1",
    "price": 25.00,
    "images": [
        "static/description/field.png",
        "static/description/choose.png",
    ],
    "currency": "EUR",
    "depends": ["web", "mail"],
    "assets": {
        "web.assets_backend": [
            "web_attachment_webcam/static/src/js/jQuery-contextMenu/jquery.contextMenu.min.css",
            "web_attachment_webcam/static/src/js/jQuery-contextMenu/jquery.contextMenu.js",
            "web_attachment_webcam/static/src/js/jQuery-contextMenu/jquery.ui.position.js",
            "web_attachment_webcam/static/src/components/attachment_webcam/attachment_webcam.js",
            "web_attachment_webcam/static/src/components/attachment_box_custom/attachment_box_custom.js",
            "web_attachment_webcam/static/src/components/attachment_webcam/attachment_webcam.xml",
            "web_attachment_webcam/static/src/components/attachment_box_custom/attachment_box_custom.xml",
        ],
    },
    "installable": True,
}
