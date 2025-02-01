# Copyright (C) 2020 Artem Shurshilov <shurshilov.a@yandex.ru>
# License OPL-1.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Allow/Disable payments,discount button,create order line,removing non-empty order,edit price button,decrease order line,removing order line,refunds,customer selection in POS",
    "summary": """
        Allow/Disable payments,discount button,create order line,
        removing non-empty order,edit price button,
        decrease order line,removing order line,refunds,
        customer selection in POS""",
    "author": "Shurshilov Artem",
    "website": "https://eurodoo.com",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Technical Settings",
    "version": "12.0.0.0",
    "license": "OPL-1",
    "price": 19,
    "currency": "EUR",
    "images": [
        "static/description/result.png",
        "static/description/settings.png",
        "static/description/youtube.png",
        "static/description/youtube.png",
    ],
    # any module necessary for this one to work correctly
    "depends": ["base", "point_of_sale"],
    "installable": True,
    # always loaded
    "data": [
        "views.xml",
    ],
}
