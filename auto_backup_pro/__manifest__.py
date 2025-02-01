# Copyright (C) 2020-2022 Artem Shurshilov <shurshilov.a@yandex.ru>
{
    "name": "Database Auto-Backup Google Drive or Local disk",
    "summary": " \
Database Auto-Backup Google Drive or Local disk \
Database Auto Backup Google Drive or Local disk \
Db Backup auto backup database auto gdrive google backup auto \
gdrive backup google remote google disk backup\
",
    "author": "EURO ODOO, Shurshilov Artem, Aurel Balanay - Evanscor Technology Solutions Inc",
    "website": "https://eurodoo.com",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Technical Settings",
    "version": "16.0.0.5",
    # "license": "OPL-1",
    "license": "LGPL-3",
    "price": 29,
    "currency": "EUR",
    "images": [
        "static/description/folder.PNG",
    ],
    # any module necessary for this one to work correctly
    "depends": ["base", "mail", "google_gdrive"],
    "external_dependencies": {
        "python": ["google-api-python-client"],
    },
    # always loaded
    "data": [
        "security/ir.model.access.csv",
        "views/backup_view.xml",
        "views/templates/auto_backup_mail_templates.xml",
        "data/backup_data.xml",
    ],
}
