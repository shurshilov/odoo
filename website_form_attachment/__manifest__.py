# -*- coding: utf-8 -*-
# Copyright 2019 Shurshilov Artem
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{
    'name': 'Website attachments contact us form',
    'summary': '''Adds field attachments to contact us form. Attach contact website form attachment file form
     files adds to website files form send file us files form''',
    'version': '12.0.0.0.2',
    'category': 'Tools',
    'website': "http://www.eurodoo.com",
    'author': 'Shurshilov Artem',
    'license': 'LGPL-3',
    #"price": 9.00,
    #"currency": "EUR",
    'application': False,
    "auto_install": False,
    'installable': True,
    'depends': ['website_form', 'website_crm', 'website_partner', 'crm'],
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
