# Copyright 2018 Onestein
# Copyright 2020 Artem Shurshilov
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Speedup Website",
    "summary": """Optimize images and lazy load images
                This module allows the user to manually
               apply compression and resize options on an image.
               This module loads images on the website lazy which means
                images are loaded only when the visitor scrolls to it (visible in viewport).
                This reduces network traffic for your website and your visitors.
                This module allows the user to manually apply compression and resize options on an image.

                To use this module, you need to:

#. Enter the website in edit mode
#. Select an image on website and double click on it
#. Now a dialog opens with all your media
#. Select tab 'Image'
#. Click on a uploaded image (images from urls do not work)
#. Click on the resize icon

Odoo Enterprise and Community versions
NGINX and Apache servers
Multi-Websites

Speed up your website
Add Lazy Loading for images and pages
Compress html
Asynchronous load javascript and/or css files
Restrict access to users who can use this module.
""",
    "category": "Website",
    "version": "12.0.1.0.1",
    "author": "Shurshilov Artem, Onestein, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "website": "https://eurodoo.com",
    "price": 49,
    "currency": "EUR",
    "depends": ["website"],
    "images": [
        "static/description/lazy.png",
    ],
    "data": ["templates/assets.xml", "templates/snippets.xml"],
    "qweb": ["static/src/xml/website_adv_image_optimization.xml"],
}
