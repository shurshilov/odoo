# -*- coding: utf-8 -*-
{
    'name': "popup_beauty",

    'summary': """
        Beauty popup window""",

    'description': """
        Very easy and beauty popup window
        from python and js javascript
    """,

    'author': "Shurshilov Artem, Savetime Tehnology",
    'website': "https://vk.com/id20132180",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Tools',
    'version': '10.0.0.1',
    'images':[
        'static/description/popup.png',
        'static/description/screen1.png',
        'static/description/example.gif',
    ],

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'views/views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
    'qweb': [
        'static/src/xml/*.xml'
    ],
    'application': False,
}