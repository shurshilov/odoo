# -*- coding: utf-8 -*-
{
    "name": "Skype field in partner form odoo 11",
    "version": "1.0.0",
    "author": "Shurshilov Artem",
    'license': 'LGPL-3',
    "category": "Tools",
#    "website": "https://apps.odoo.com/apps/browse?repo_maintainer_id=160431",
    'website': "http://www.eurodoo.com",
    #'price': 9.00,
    #'currency': 'EUR',
    "depends": ['web'],
    "images": [
	    'static/description/module.png',
	    'static/description/field.png'
	    'static/description/skype.png'
    ],
    "data": [
        'views.xml',
        'data.xml',
    ],
    "qweb": [
        'static/src/xml/base.xml',
    ],
    'installable': True
}
