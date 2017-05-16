# -*- coding: utf-8 -*-
{
    'name': "Document existing",
    'summary': "Модуль прикрепления объектов",
    'description': "Модуль позволяет прикреплять объекты из добавленных ранее",
    'author': "Alexander",
    'website': "alexander590@mail.ru",
    'category': 'Tools',
    'version': '0.1',
    'license': 'AGPL-3',
    'depends': ['document'],
    'data': [
        'view/document_existing_view.xml',
    ],
    'qweb': [
        'static/src/xml/url.xml',
    ],
    "installable": True,
}