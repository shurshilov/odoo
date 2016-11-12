# -*- coding: utf-8 -*-
{
    "name": """Show forward button""",
    "summary": """Forward message to other email or partner and user""",
    "category": "Discuss",
    "images": [],
    "version": "1.0.0",

    "author": "Artem Shurshilov",
    "website": "https://vk.com/id20132180",
    "license": "LGPL-3",

    "depends": [
        "mail_base",
    ],
    "external_dependencies": {"python": [], "bin": []},
    "data": [
        'templates.xml'
    ],
    "qweb": [
        "static/src/xml/forward_button.xml",
    ],
    "demo": [],
    "installable": True,
    "auto_install": False,
}
