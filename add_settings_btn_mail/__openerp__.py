# -*- coding: utf-8 -*-
# Copyright (C) 2018 Shurshilov Artem <shurshilov.a@yandex.ru>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Hide notification chatter',
    'summary': """Widget add hide notification checkbox in chatter""",
    'description': """
Widget add hide notification checkbox in chatter
==============================================
    * Save hide status in database
    * Control hide notification for every record
    * Аast work
    * Кemembering the previous press
    * Рides technical comments

""",
    'author': 'Shurshilov Artem',
#    "website": "https://vk.com/id20132180",
    'website': "http://www.eurodoo.com",
    
    # Categories can be used to filter modules in modules listing
    'category': "Tools, mail",
	   'version': '1.0',
    # any module necessary for this one to work correctly
    'depends': ['base','mail','hr'],    
    "license": "LGPL-3",
#    'price': 9.99,
#    'currency': 'EUR',
    # always loaded
    'images':[
            'static/description/stock_open.png',
    	    'static/description/stock_open2.png',
	        'static/description/stock_cursor.png',
    ],
    'data': [ 'views/add_settings_btn_mail.xml', ],   
    'qweb': [ 'static/src/xml/settings.xml', ],
    'installable': False,
    'application': False,
    # If it's True, the modules will be auto-installed when all dependencies
    # are installed
    'auto_install': False,
}