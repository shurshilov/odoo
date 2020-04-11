# -*- coding: utf-8 -*-
# Copyright 2017 IT Projects LLC.
# Copyright 2017-2020 Artem Shurshilov
{
    'name': "Website Search Product Tags Fork",
    'summary': """Search website products by tags""",
    'category': 'eCommerce',
    'version': '13.0.0.0',
    'application': False,
    'author': 'Shurshilov Artem,IT-Projects LLC',
    'license': 'LGPL-3',
    'website': "http://www.eurodoo.com",
    'price': 30.0,
    'currency': 'EUR',
    'images': [
        'static/description/search.png',
        'static/description/product_tags.png',
        'static/description/web_search_tags.png',
    ],
    'depends': ['website_sale', 'product_tags_fork', 'stock'],
    'auto_install': False,
    'installable': True,
}
