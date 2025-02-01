# Copyright (C) 2019 Artem Shurshilov <shurshilov.a@yandex.ru>
# License OPL-1.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "excel report template ms populating (EXCEL,LIBRE,OPENOFFICE)",
    "summary": " \
Do report template in docx and see result in excel with odoo data \
Populating MS Excel Templates with Python microsoft libreoffice openofiice \
doc docx template doc templates docx template docx ms docx microsoft word \
report to excel report to xlsx report xlsx template reports excel reports xlsx \
",
    "author": "EURO ODOO, Shurshilov Artem",
    "website": "https://eurodoo.com",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Technical Settings",
    "version": "15.3.1.2",
    "license": "OPL-1",
    "price": 49,
    "currency": "EUR",
    "images": [
        "static/description/template.png",
        "static/description/report_form.png",
        "static/description/result.png",
        "static/description/report_form.png",
    ],
    # any module necessary for this one to work correctly
    "depends": ["base", "web"],
    "external_dependencies": {"python": ["openpyxl"]},
    "installable": True,
    # always loaded
    "data": [
        "views/views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "excel_report/static/**/*",
        ],
    },
}
