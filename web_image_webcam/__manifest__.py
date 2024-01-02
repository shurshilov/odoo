# Copyright 2022 Shurshilov Artem<shurshilov.a@yandex.ru>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    "name": "Web Widget - Image WebCam",
    "summary": """Allows to take image with WebCam
    [TAGS] web camera web foto web photo web images camera
    image snapshot web snapshot webcam snapshot picture web contact
    image web product image online mobile web image produt mobile""",
    "version": "16.1.3",
    "category": "web",
    "website": "https://www.eurodoo.com",
    "live_test_url": "https://eurodoo.com/login_employee?login=demo1&password=demo777",
    "author": "Shurshilov Artem",
    "license": "OPL-1",
    "price": 19.00,
    "images": [
        "static/description/field.png",
        "static/description/choose.png",
    ],
    "currency": "EUR",
    "depends": [
        "web",
    ],
    "assets": {
        "web.assets_backend": [
            # "web_image_webcam/static/src/**/*.css",
            "web_image_webcam/static/src/js/webcam_dialog.js",
            "web_image_webcam/static/src/js/image_field.js",
            "web_image_webcam/static/src/xml/web_widget_image_webcam.xml",
        ],
    },
    "installable": True,
}
