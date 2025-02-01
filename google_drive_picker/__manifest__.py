# Copyright (C) 2020-2021 Artem Shurshilov <shurshilov.a@yandex.ru>
# License OPL-1.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Google Drive Picker upload attachments",
    "summary": "Google Drive Picker upload attachments download file \
search content search content pdf,image,photo and other attachment gdrive attachment \
attachments gdrive attachments chatter gdrive chatter record gdrive record \
from google to odoo files gdrive files file gdrive file \
attachment google attachments google cloud attachment cloud \
attachments google integration google intergrations\
",
    "author": "EURO ODOO, Shurshilov Artem",
    "website": "https://eurodoo.com",
    "live_test_url": "https://eurodoo.com/login_employee?login=demo1&amp;password=demo1",
    # Categories can be used to filter modules in modules listing
    "category": "Extra Tools",
    "version": "14.3.1.5",
    # any module necessary for this one to work correctly
    "depends": ["web", "mail"],
    "license": "OPL-1",
    "price": 39,
    "currency": "EUR",
    "images": [
        "static/description/preview.gif",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/assets.xml",
        "views/res_config_settings_views.xml",
        "views/gdrive_folder_pattern_view.xml",
    ],
    "qweb": [
        "static/src/xml/gdrive.xml",
    ],
    "installable": True,
    "application": False,
    # If it's True, the modules will be auto-installed when all dependencies
    # are installed
    "auto_install": False,
}
