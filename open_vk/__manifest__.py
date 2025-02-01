{
    "name": "VK.com authorize",
    "summary": """
    Authorize in Odoo from social network VK.COM""",
    "description": """
        Protocol Oauth2, auth with access token
    """,
    "author": "Shurshilov Artem",
    "website": "https://www.odoo.com/apps/modules/browse?search=shursh",
    "license": "LGPL-3",
    #'price': 49.00,
    #'currency': 'EUR',
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    "category": "Extra Tools",
    "version": "12.0.1.0.0",
    "images": [
        "static/description/vk.jpg",
        "static/description/vkauth.png",
        "static/description/signin.png",
    ],
    # any module necessary for this one to work correctly
    "depends": ["base", "web", "base_setup", "auth_signup", "auth_oauth"],
    # always loaded
    "data": [
        "security/ir.model.access.csv",
        "views/views.xml",
        "views/templates.xml",
    ],
    # only loaded in demonstration mode
    "demo": [
        "demo/demo.xml",
    ],
}
