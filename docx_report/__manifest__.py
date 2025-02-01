# Copyright (C) 2019 Artem Shurshilov <shurshilov.a@yandex.ru>
# License OPL-1.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "docx report template ms populating (WORD,LIBRE,OPENOFFICE)",
    "summary": """
        Do report template in docx and see result in docx with odoo data
        Populating MS Word Templates with Python microsoft libreoffice openofiice
        doc docx template doc templates docx template docx ms docx microsoft word""",
    "author": "Shurshilov Artem",
    "website": "https://eurodoo.com",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Technical Settings",
    "version": "13.2.4.0",
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
    "installable": True,
    # always loaded
    "data": [
        "views/views.xml",
    ],
    # 'qweb': [
    #     "static/src/xml/base.xml",
    # ],
}
