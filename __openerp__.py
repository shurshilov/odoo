# -*- coding: utf-8 -*-
# Copyright (C) 2016 Artem Shurshilov <shurshilov.a@yandex.ru>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Mail URL attachment',
    'summary': """Adds attachment url and filename to upload message (see screenshots) """,
    'description': """
This is extension for module mail
==============================================
* ATTACHMENTS TO MESSAGE:
    * URL
        * Add link (url) e.g. www.google.com as attachmentin message 
        * When you click on the link then you are automatically taken to the site in a new tab
        * Links also have a name as files
    * FILE
        * Added file name when downloading a file, you can change it dynamically.
        * Stored in the database as a real file name and the name that you entered
        * If the file name has not been entered, the file name assigned by the operating system
    * EDIT
        * Edit all attachments dynamically. (new buttom)

""",
    'author': 'Shurshilov Artem',
    "website": "https://vk.com/id20132180",
    
    # Categories can be used to filter modules in modules listing
    'category': "mail",
	'version': '1.0',
    # any module necessary for this one to work correctly
    'depends': ['web', 'mail'],    
    "license": "LGPL-3",
#    'price': 9.99,
#    'currency': 'EUR',
    # always loaded
    'images':[
    	    'static/description/3.png',
	    'static/description/4.png',
	    'static/description/1.png',
	    'static/description/2.png',
    ],
    'data': [ 'wizard/mail_url_view.xml', ],   
    'qweb': [ 'static/src/xml/url.xml',
              'static/src/xml/mail.xml',
    ],
    'installable': True,
    'application': False,
    # If it's True, the modules will be auto-installed when all dependencies
    # are installed
    'auto_install': False,
}
