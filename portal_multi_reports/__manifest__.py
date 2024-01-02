# Copyright (C) 2021-2023 Artem Shurshilov <shurshilov.a@yandex.ru>
# License OPL-1.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Portal multi reports",
    "summary": " \
Add selection for portal reports \
User can seletc which report print \
Also administrator manage which repors available for portal selection and printing \
",
    "author": "EURO ODOO, Shurshilov Artem",
    "maintainer": "EURO ODOO",
    "website": "https://eurodoo.com",
    "live_test_url": "https://eurodoo.com",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Document Management",
    "version": "16.0.0",
    "license": "OPL-1",
    "price": 49.0,
    "currency": "EUR",
    "images": [
        "static/description/preview.png",
    ],
    # any module necessary for this one to work correctly
    "depends": ["base", "web", "sale"],
    # always loaded
    "data": [
        "views/views.xml",
        "views/portal.xml",
    ],
}
