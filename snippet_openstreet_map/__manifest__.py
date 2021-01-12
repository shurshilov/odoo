# -*- coding: utf-8 -*-
# Copyright (C) 2020 Shurshilov Artem <shurshilov.a@yandex.ru>
# License OPL-1.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': "Openstreet Leaflet Map Snippet",

    'summary': """
        Adds FREE leaflet OSM map on website as snippet
    [TAGS] website maps leaflet osm map free map osm leaflet
    map leaflet map maps lealet website openstreet map widget""",

    'author': "Shurshilov Artem",
    'website': "http://www.eurodoo.com",
    # "live_test_url": "https://www.eurodoo.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Website',
    'version': '12.0.0.0',
    "license": "OPL-1",
    'price': 49,
    'currency': 'EUR',
    'images': [
        'static/description/preview.gif',
        'static/description/face_control.png',
        'static/description/face_control.png',
        'static/description/face_control.png',
    ],

    # any module necessary for this one to work correctly
    'depends': ['website'],

    # always loaded
    'data': [
        'views/assets.xml',
        'views/s_google_map.xml',
    ],
    'qweb': [
        "static/src/xml/attendance.xml",
        "static/src/xml/kiosk.xml",
    ],
}
