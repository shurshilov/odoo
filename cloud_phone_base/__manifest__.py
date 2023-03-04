# -*- coding: utf-8 -*-
# Copyright (C) 2022 Artem Shurshilov <shurshilov.a@yandex.ru>
# License OPL-1.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Cloud phone base",
    "summary": """
        Cloud phone base functionality
        store, view, filter, delete calls
        """,
    "author": "EURO ODOO, Shurshilov Artem",
    "website": "https://eurodoo.com",
    "live_test_url": "https://eurodoo.com/blog",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Tools",
    "version": "14.3.0.1",
    "license": "OPL-1",
    "support": "shurshilov.a@yandex.ru",
    "price": 39,
    "currency": "EUR",
    "images": [
        "static/description/preview.png",
    ],
    # any module necessary for this one to work correctly
    "depends": ["base", "web", "hr", "sale", "crm", "attachments_widgets"],
    "installable": True,
    # always loaded
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/assets.xml",
        "views/connectors.xml",
        "views/numbers.xml",
        "views/calls.xml",
        "views/events.xml",
        "views/menu.xml",
        "views/hr_employee.xml",
        "views/res_partner.xml",
        "views/sale_order.xml",
        "views/crm_lead.xml",
        "data/scheduler_data.xml",
    ],
    'qweb': [
        "static/src/xml/call_dialog.xml",
    ],
}
