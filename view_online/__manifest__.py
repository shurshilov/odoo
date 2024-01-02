# Copyright (C) 2021 Artem Shurshilov <shurshilov.a@yandex.ru>
# License OPL-1.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "View online form collaborate work",
    "summary": """shows users who are online working with the form,
    collaborate, jointly, in common, mutually""",
    "author": "EURO ODOO, Shurshilov Artem, Stanislav Tuilenev",
    "website": "https://eurodoo.com",
    # "live_test_url": "https://eurodoo.com/login_employee?login=demo1&amp;password=demo1",
    # Categories can be used to filter modules in modules listing
    "category": "Extra Tools",
    "version": "14.0.2",
    # any module necessary for this one to work correctly
    "depends": ["web", "bus"],
    "license": "OPL-1",
    "price": 49,
    "currency": "EUR",
    "images": [
        "static/description/result2.png",
    ],
    "data": [
        "views/assets.xml",
    ],
    "installable": True,
    "application": False,
    # If it's True, the modules will be auto-installed when all dependencies
    # are installed
    "auto_install": False,
}
