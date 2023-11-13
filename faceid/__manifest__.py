# Copyright (C) 2019 Artem Shurshilov <shurshilov.a@yandex.ru>
# License OPL-1.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "face id",
    "summary": """
        FACE ID""",
    "author": "EURO ODOO, Shurshilov Artem",
    "website": "https://eurodoo.com",
    "live_test_url": "https://eurodoo.com",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Technical Settings",
    "version": "0.0.1",
    "license": "OPL-1",
    "price": 299,
    "currency": "EUR",
    "images": [
        "static/description/template.png",
        "static/description/report_form.png",
        "static/description/result.png",
        "static/description/report_form.png",
    ],
    # any module necessary for this one to work correctly
    "depends": ["base", "web", "mail"],
    "installable": False,
    # always loaded
    "data": [
        "security/faceid_access_groups.xml",
        "security/ir.model.access.csv",
        "views/views.xml",
    ],
    # 'qweb': [
    #     "static/src/xml/base.xml",
    # ],
}
