# Copyright (C) 2019-2022 Artem Shurshilov <shurshilov.a@yandex.ru>
# License OPL-1.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "docx report template ms populating (WORD,LIBRE,OPENOFFICE)",
    "summary": """
        Do report template in docx and see result in docx with odoo data
        Populating MS Word Templates with Python microsoft libreoffice openofiice
        doc docx template doc templates docx template docx ms docx microsoft word
        Template Report DOCX Is Easy an elegant and scalable solution to
        design reports using Microsoft Office Export data all objects odoo to Microsoft Office
        output files docx""",
    "author": "EURO ODOO, Shurshilov Artem",
    "maintainer": "EURO ODOO",
    "website": "https://eurodoo.com",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Technical Settings",
    "version": "16.0.0.5",
    "license": "OPL-1",
    "price": 39,
    "currency": "EUR",
    "images": [
        "static/description/template.png",
        "static/description/report_form.png",
        "static/description/result.png",
        "static/description/report_form.png",
    ],
    # any module necessary for this one to work correctly
    "depends": ["base", "web"],
    "installable": True,
    # always loaded
    "data": [
        "views/views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "docx_report/static/**/*",
        ],
    },
}
