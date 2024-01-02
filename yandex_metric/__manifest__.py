# Copyright 2019 Artem Shurshilov
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{
    "name": """FREE website session replays and metric""",
    "summary": """FREE feauters webvisor sessions replay website and backend users
        best metrics and repors. Best integration modules""",
    "version": "12.0.1",
    "category": "Website",
    "website": "https://eurodoo.com",
    "author": "Shurshilov Artem",
    "license": "LGPL-3",
    # "price": 29.00,
    # "currency": "EUR",
    "application": False,
    "auto_install": False,
    "installable": True,
    "depends": ["base", "website"],
    "data": [
        "templates.xml",
        "res_config_settings_views.xml",
    ],
    "images": [
        "static/description/web_visor_backend.png",
        "static/description/map_click.png",
        "static/description/dashboard.png",
    ],
    "external_dependencies": {"python": [], "bin": []},
}
