# -*- coding: utf-8 -*-

{
    'name': 'URL attachment',
	'version': '0.1',
	'depends': ['mail'],
    'author': 'Shurshilov Artem',
    'category': 'Mail extension',
    'description': """
Add links to message
==================================================================
    """,
    'depends': ['web',  ],
    'website': 'https://github.com/shurshilov',
    'data': [ 'wizard/document_url_view.xml',            
 #             'static/src/xml/url.xml',
    ],
   
    'qweb': [ 'static/src/xml/url.xml',
              'static/src/xml/mail.xml',
    ],
}
