# Copyright 2004-2010 OpenERP SA (<http://www.openerp.com>)
# Copyright 2011-2015 Serpent Consulting Services Pvt. Ltd.
# Copyright 2017 Tecnativa - Vicent Cubells
# Copyright 2019 Open Source Integrators
# Copyright 2020 Shurshilov Artem <shurshilov.a@yandex.ru>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Web Widget Digitized Signature",
    "summary": "Res users Digitized Signature",
    "author": "Serpent Consulting Services Pvt. Ltd., "
    "Agile Business Group, "
    "Tecnativa, "
    "Odoo Community Association (OCA)"
    "Shurshilov Artem",
    "maintainer": "EURO ODOO",
    "website": "https://eurodoo.com",
    "live_test_url": "https://eurodoo.com",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Document Management",
    "version": "17.0.0.0.0",
    "license": "AGPL-3",
    # "price": 19.0,
    # "currency": "EUR",
    "images": ["static/description/sign.png"],
    # any module necessary for this one to work correctly
    "depends": ["base", "web", "mail"],
    # always loaded
    "data": [
        "views/res_users_view.xml",
    ],
}
