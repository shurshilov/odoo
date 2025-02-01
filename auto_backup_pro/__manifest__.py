# Copyright (C) 2020 Artem Shurshilov <shurshilov.a@yandex.ru>
# License LGPL-3 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Database Auto-Backup Google Drive or Local disk",
    "summary": " \
Database Auto-Backup Google Drive or Local disk \
Database Auto Backup Google Drive or Local disk \
Db Backup auto backup database auto gdrive google backup auto \
",
    "author": "Shurshilov Artem, Aurel Balanay - Evanscor Technology Solutions Inc",
    "website": "https://eurodoo.com",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Technical Settings",
    "version": "14.0.0.3",
    # "license": "OPL-1",
    "license": "LGPL-3",
    "price": 49,
    "currency": "EUR",
    "images": [
        "static/description/folder.PNG",
    ],
    # any module necessary for this one to work correctly
    "depends": ["base", "mail", "google_drive"],
    # always loaded
    "data": [
        "security/ir.model.access.csv",
        "views/backup_view.xml",
        "views/templates/auto_backup_mail_templates.xml",
        "data/backup_data.xml",
    ],
}
