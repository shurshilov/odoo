# Copyright (C) 2020 Artem Shurshilov <shurshilov.a@yandex.ru>
# License OPL-1.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "VOIP FREE out of box video audio remote desktop jitsi meeting online",
    "summary": """
        VOIP FREE out of box video audio remote desktop jitsi meeting
         Full integration of Jitsi Video Conferencing jitsi meet jitsi voip jitsi call jitsi video
         jitsi integration jitsi meet jitsi meeting jitsi audio jitsi calls jitsi desktop
         jitsi odoo jitsi mail jitsi mail""",
    "author": "EURO ODOO, Shurshilov Artem",
    "maintainer": "EURO ODOO",
    "website": "https://eurodoo.com",
    # "live_test_url": "https://eurodoo.com",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Other Extra Rights",
    "version": "1.0.2",
    "license": "OPL-1",
    "price": 50,
    "currency": "EUR",
    "images": [
        "static/description/Odoo-VOIP-video-audio-screen-sharing-FREE.gif",
    ],
    # any module necessary for this one to work correctly
    "depends": ["base", "mail"],
    # always loaded
    "data": [
        # 'views/assets.xml',
        "views/res_config_settings_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            # 'mail_remote_desktop/static/src/js/lib/meet.jit.si.external_api.js',
            "https://meet.jit.si/external_api.js",
            "mail_remote_desktop/static/src/js/mail_remote_desktop.js",
            "mail_remote_desktop/static/src/xml/mail.xml",
        ],
        # 'web.assets_qweb': [
        # ],
    },
    # 'qweb': [
    #     "static/src/xml/mail.xml",
    # ],
}
