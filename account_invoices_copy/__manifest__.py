# -*- coding: utf-8 -*-
# Copyright 2019 Artem Shurshilov
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    'name': "Invoice mass copy with new date",  # It must be non-technical name of the module
    'summary': """
        The module adds the ability to copy vendor accounts.
        When copying, you can set the accounting date in the budget and the date of payment.
        The copied account takes the draft status, regardless of the status of the copied account.
        Responsible in the copied account will be the user who launched the action.
    """,  # describe here which problems solved by module
    'author': "Shurshilov Artem",
    'support': "shurshilov.a@yandex.ru",
#    'website': "https://vk.com/id20132180",
    'website': "http://www.eurodoo.com",
    "license": "LGPL-3",
    'category': 'Accounting',
    'version': '13.0.0.0',  # odoo.x.y.z; z - bags, y - feautures, x - model or view big changes
    'depends': ['base', 'account'],  # any odoo module necessary for this one to work correctly
    'data': [  # always loaded
        'views/account_invoice_views.xml',
        'wizard/account_invoice_copy_wizard_views.xml',
    ],
    'images': [
        'static/description/screen.png',
        'static/description/screen1.png',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
