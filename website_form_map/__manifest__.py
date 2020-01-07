# -*- coding: utf-8 -*-
# Copyright 2019 Artem Shurshilov
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{
    'name': 'Website widget map (OSM and leaflet)',
    'summary': '''Adds FREE leaflet OSM map on contact us form''',
    'version': '12.0.0.1.1',
    'category': 'Tools',
    'website': "http://www.eurodoo.com",
    'author': 'Shurshilov Artem',
    'license': 'LGPL-3',
    #"price": 9.00,
    #"currency": "EUR",
    'application': False,
    "auto_install": False,
    'installable': True,
    'depends': ['base','website'],
    'data': [
        'views/website_crm_templates.xml',
    ],
    'images':[
            'static/description/field.png',
            'static/description/choose.png',
            'static/description/result.png',
    ],
    "external_dependencies": {"python": [], "bin": []},
}
