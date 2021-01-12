# -*- coding: utf-8 -*-
# Copyright 2016-2017 LasLabs Inc.
# Copyright 2017-2018 Shurshilov Artem
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{
    'name': 'Widget image tools',
    'summary': 'Provides web widget for image editing and adds it to standard'
               ' image widget as modal',
    'version': '9.0.1.0.1',
    'category': 'Tools',
#    'website': 'https://vk.com/id20132180',
    'website': "http://www.eurodoo.com",
    'author': 'Shurshilov Artem',
    'license': 'LGPL-3',
    "price": 29.00,
    "currency": "EUR",
    'application': False,
    "auto_install": False,
    'installable': False,
    'depends': [
        'web',
    ],
    'data': [
        'views/assets.xml',
        'wizards/darkroom_modal.xml',
    ],
    'qweb': [
        'static/src/xml/field_templates.xml',
    ],
    'images':[
            'static/description/Edit.png',
    ],
    "post_load": "post_load",
    "pre_init_hook": None,
    "post_init_hook": None,
    "external_dependencies": {"python": [], "bin": []},
}
