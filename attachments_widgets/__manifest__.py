{
    "name": "Attachments widgets (Audio etc..)",
    "summary": """
        Attachments widgets audio ant others
        """,
    "author": "EURO ODOO, Shurshilov Artem",
    "website": "https://eurodoo.com",
    "live_test_url": "https://eurodoo.com/blog",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Tools",
    "version": "0.0.0",
    "license": "OPL-1",
    "support": "shurshilov.a@yandex.ru",
    # "price": 9,
    # "currency": "EUR",
    "images": [
        "static/description/audio widget tree.png",
    ],
    "assets": {
        "web.assets_backend": [
            "attachments_widgets/static/src/components/audio_widgets.js",
            "attachments_widgets/static/src/components/audio.xml",
            # "attachments_widgets/static/src/js/audio_widgets.js",
            # "attachments_widgets/static/src/js/video_widgets.js",
        ],
    },
    "auto_install": False,
    "installable": True,
}
