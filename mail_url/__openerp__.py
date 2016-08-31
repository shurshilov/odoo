# -*- coding: utf-8 -*-

{
    'name': 'Mail URL attachment',
	'version': '0.1',
    'depends': ['web', 'mail'],
    'author': 'Shurshilov Artem',
    'category': 'Mail extension odoo v.8',
    'description': """
Add links to message
==================================================================
    """,
    'website': 'https://github.com/shurshilov',
    'data': [ 'wizard/mail_url_view.xml', ],   
    'qweb': [ 'static/src/xml/url.xml',
              'static/src/xml/mail.xml',
    ],
}
