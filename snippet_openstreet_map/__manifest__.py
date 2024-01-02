# Copyright (C) 2020 Shurshilov Artem <shurshilov.a@yandex.ru>
# License OPL-1.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Openstreet Leaflet Map Snippet",
    "summary": """
        Adds FREE leaflet OSM map on website as snippet
    [TAGS] website maps leaflet osm map free map osm leaflet
    map leaflet map maps lealet website openstreet map widget""",
    "author": "Shurshilov Artem",
    "website": "http://www.eurodoo.com",
    # "live_test_url": "https://www.eurodoo.com",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Website",
    "version": "15.0.1",
    "license": "OPL-1",
    "price": 49,
    "currency": "EUR",
    "images": [
        "static/description/preview.gif",
        "static/description/face_control.png",
        "static/description/face_control.png",
        "static/description/face_control.png",
    ],
    # any module necessary for this one to work correctly
    "depends": ["website"],
    # always loaded
    "data": [
        # 'views/assets.xml',
        "views/s_google_map.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "snippet_openstreet_map/static/src/js/lib/leaflet.js",
            "snippet_openstreet_map/static/src/js/s_google_map_frontend.js",
            "snippet_openstreet_map/static/src/css/leaflet.css",
        ],
        # 'website.assets_editor': [
        #     'snippet_openstreet_map/static/src/js/s_google_map_editor.js',
        # ],
        # 'web.assets_qweb': [
        #     'snippet_openstreet_map/static/src/**/*.xml',
        # ],
    },
}
