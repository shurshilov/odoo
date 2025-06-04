{
    "name": "Geo Coordinates Yandex Widget Map",
    "version": "16.0.1.0.1",
    "depends": ["web"],
    "author": "EURO ODOO, Shurshilov Artem",
    "maintainer": "EURO ODOO",
    "website": "https://eurodoo.com",
    "category": "Tools",
    "description": "Adds a Yandex Map widget to select and save geo coordinates",
    "assets": {
        "web.assets_backend": [
            # "https://api-maps.yandex.ru/2.1/?lang=ru_RU",
            "yandex_geo_widget/static/src/js/geo_map_widget.js",
            "yandex_geo_widget/static/src/xml/geo_map_widget.xml",
        ]
    },
    "installable": True,
    "application": False,
    "auto_install": False,
}
