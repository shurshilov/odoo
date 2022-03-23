# -*- coding: utf-8 -*-
# Copyright (C) 2020-2022 Artem Shurshilov <shurshilov.a@yandex.ru>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': "Real multi images backend and swipe images",

    'summary': """
        Real multi images backend and swipe images
        multi website multi images website image multi website several images 
        website several image website swiper photo website swipe photo website
        touch images website multi pictures website picture site multi pictures
        site multi images ecommerce multi images website sale multi images
        website
        """,

    'author': "Shurshilov Artem",
    'website': "https://eurodoo.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'eCommerce',
    'version': '15.2.0.0',
    "license": "OPL-1",
    "support": "shurshilov.a@yandex.ru",
    # 'price': 19,
    # 'currency': 'EUR',
    'images':[
        'static/description/backend.gif',
    ],

    # any module necessary for this one to work correctly
    #'depends': ['website_sale'],
    'installable': True,

    'assets': {
        'web.assets_backend': [
            "swipe_images_backend/static/src/libs/**/*",
            "swipe_images_backend/static/src/js/**/*",
        ],
        'web.assets_qweb': [
            'swipe_images_backend/static/src/xml/image.xml',
        ]
    },
}
