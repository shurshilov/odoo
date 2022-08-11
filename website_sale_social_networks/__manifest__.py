# -*- coding: utf-8 -*-
# Copyright (C) 2020-2022 Artem Shurshilov <shurshilov.a@yandex.ru>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': "Social manager website 35+ top messangers and social networks svg",

    'summary': """
        Professional social manager 
        website 35+ top messangers and social networks svg
        launch application by click 
        customize icon features
        facebook with background
        twitter with background
        google-plus with background
        linkedin with background
        round dribbble with background
        round github with background
        round behance with background
        round codepen with background
        rounded instagram with background
        rounded pinterest with background
        rounded buffer with background
        rounded vk with background
        rounded medium with background
        rounded tumblr with background
        rounded rss with background
        rounded flickr with background
        rounded snapchat with background
        rounded whatsapp with background
        rounded reddit with background
        rounded vine with background
        rounded youtube with background
        rounded spotify with background
        rounded soundcloud with background
        rounded amazon with background
        google-plus alternates with background
        facebook alternates with background
        youtube alternates with background
        soundcloud alternates with background
        reddit alternates with background
        github alternates with background
        app-store with background
        google-play with background
        email generic with background
        location generic with background
        phone generic with background
        """,

    'author': "Shurshilov Artem",
    'website': "https://eurodoo.com",
    'live_test_url': "https://eurodoo.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'eCommerce',
    'version': '15.0.0.1',
    "license": "LGPL-3",
    "support": "shurshilov.a@yandex.ru",
    # 'price': 19,
    # 'currency': 'EUR',
    'images': [
        'static/description/button.png',
        'static/description/result.png',
        'static/description/result.png',
    ],

    # any module necessary for this one to work correctly
    'depends': ['web', 'website'],
    'installable': True,

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'website_sale_social_networks.xml',
        'data.xml',
    ],

    'assets': {
        'web.assets_frontend': [
            'website_sale_social_networks/static/src/css/website_sale_social_networks.css',
    ],

    },
    # 'qweb': [
    #     "static/src/xml/base.xml",
    # ],
}
