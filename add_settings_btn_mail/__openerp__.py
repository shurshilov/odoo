# -*- coding: utf-8 -*-
# Copyright (C) 2018 Artem Shurshilov <shurshilov.a@yandex.ru>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Widget add settings button mail followers',
    'summary': """Adds functional preview (open/popup) to mail followers comments """,
    'description': """
This is extension for <field widget="image"> widget image
==============================================
* STOCK and CONTACT example:
    * open image on click in original size in popup
    * close on close button
    * close on click on/out image

""",
    'author': 'Shurshilov Artem',
    "website": "https://vk.com/id20132180",
    
    # Categories can be used to filter modules in modules listing
    'category': "Tools",
	   'version': '1.0',
    # any module necessary for this one to work correctly
    'depends': ['base','mail','hr'],    
    "license": "LGPL-3",
#    'price': 9.99,
#    'currency': 'EUR',
    # always loaded
    'images':[
    	    'static/description/stock_open2.png',
	        'static/description/stock_open.png',
	        'static/description/stock_cursor.png',
    ],
    'data': [ 'views/add_settings_btn_mail.xml', ],   
    'qweb': [ 'static/src/xml/settings.xml', ],
    'installable': True,
    'application': False,
    # If it's True, the modules will be auto-installed when all dependencies
    # are installed
    'auto_install': False,
}