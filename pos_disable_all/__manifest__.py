# Copyright (C) 2020-22 Artem Shurshilov <shurshilov.a@yandex.ru>
# License OPL-1.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Allow/Disable payments,discount button,create order line,removing non-empty order,edit price button,decrease order line,removing order line,refunds,customer selection in POS",
    "summary": """
        Allow/Disable payments,discount button,create order line,
        removing non-empty order,edit price button,
        decrease order line,removing order line,refunds,
        customer selection in POS
        pos_user_access pos user access
        This module allows you to give access in point of sale
        Pos change user wise access
        We can change access according to user at run time so we don't want to refresh POS
        Configuration for POS access
        Numpad is not allowed for this user
        Change access according to user
        Easy way to give user access
        User Access to POS Closing
        User Access to Order Deletion
        User Access to Order Line Deletion
        User Access to Order Payment
        User Access to Discount Application
        User Access to Price Change
        User Access to Decreasing Quantity
        User access/restriction seemless integration to POS interface""",
    "author": "EURO ODOO, Shurshilov Artem",
    "website": "https://eurodoo.com",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Technical Settings",
    "version": "15.4.0",
    "license": "OPL-1",
    "price": 25,
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
    "assets": {
        "point_of_sale.assets": [
            "pos_disable_all/static/src/js/pos_disable_all.js",
            "pos_disable_all/static/src/css/pos.css",
        ],
    },
    # always loaded
    "data": [
        "views.xml",
    ],
}
