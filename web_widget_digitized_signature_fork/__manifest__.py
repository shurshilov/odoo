# Copyright 2004-2010 OpenERP SA (<http://www.openerp.com>)
# Copyright 2011-2015 Serpent Consulting Services Pvt. Ltd.
# Copyright 2017 Tecnativa - Vicent Cubells
# Copyright 2019 Open Source Integrators
# Copyright 2020 Shurshilov Artem <shurshilov.a@yandex.ru>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Web Widget Digitized Signature',
    'version': '13.0.1.0.0',
    'author': 'Serpent Consulting Services Pvt. Ltd., '
              'Agile Business Group, '
              'Tecnativa, '
              'Odoo Community Association (OCA)'
              'Shurshilov Artem',
    'website': 'www.eurodoo.com',
    'license': 'AGPL-3',
    'category': 'Web',
    'depends': [
        'web',
        'mail',
    ],
    'price': 19,
    'currency': 'EUR',
    'data': [
        'views/web_digital_sign_view.xml',
        'views/res_users_view.xml',
    ],
        'images': [
        'static/description/sign.png',
        'static/description/sign.png',
        'static/description/sign.png',
    ],
    'qweb': [
        'static/src/xml/digital_sign.xml',
    ],
    'installable': True,
    'development_status': 'Production/Stable',
    'maintainers': ['mgosai'],
}
