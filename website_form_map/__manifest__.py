# -*- coding: utf-8 -*-
# Copyright 2019 Shurshilov Artem
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{
    'name': 'Website widget map (OSM and Leaflet)',
    'summary': '''Adds FREE leaflet OSM map on contact us form
    [TAGS] website maps leaflet osm map free map osm leaflet
    map leaflet map maps lealet website openstreet map widget''',
    'version': '13.0.0.1.1',
    'category': 'Tools',
    'website': "http://www.eurodoo.com",
    'author': 'Shurshilov Artem',
    'license': 'LGPL-3',
    #"price": 9.00,
    #"currency": "EUR",
    'application': False,
    "auto_install": False,
    'installable': True,
    'depends': ['base','website','website_form', 'website_crm', 'website_partner', 'crm'],
    'data': [
        'views/website_crm_templates.xml',
    ],
    'images':[
            'static/description/result.png',
            'static/description/settings.png',
            #'static/description/result.png',
    ],
    "external_dependencies": {"python": [], "bin": []},
}
