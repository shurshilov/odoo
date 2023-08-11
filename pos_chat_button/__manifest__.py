# Copyright (C) 2020-2022 Artem Shurshilov <shurshilov.a@yandex.ru>
# Odoo Proprietary License v1.0

# This software and associated files (the "Software") may only be used (executed,
# modified, executed after modifications) if you have purchased a valid license
# from the authors, typically via Odoo Apps, or if you have received a written
# agreement from the authors of the Software (see the COPYRIGHT file).

# You may develop Odoo modules that use the Software as a library (typically
# by depending on it, importing it and using its resources), but without copying
# any source code or material from the Software. You may distribute those
# modules under the license of your choice, provided that this license is
# compatible with the terms of the Odoo Proprietary License (For example:
# LGPL, MIT, or proprietary licenses similar to this one).

# It is forbidden to publish, distribute, sublicense, or sell copies of the Software
# or modified copies of the Software.

# The above copyright notice and this permission notice must be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
{
    "name": "Chat Point of sale",
    "summary": " \
Top 30+ best feauters to manage your attachments \
attachments tags attachment tag \
Drag and Drop multiple attachments webcam attachments pos chat chat pos \
point of sale chat chat point of sale sale chat sale    \
",
    "author": "EURO ODOO, Shurshilov Artem",
    "website": "https://eurodoo.com",
    # "live_test_url": "https://eurodoo.com/login_employee?login=demo1&password=demo1",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Point of sale",
    "version": "15.0.0.1",
    "license": "OPL-1",
    "price": 49,
    "currency": "EUR",
    "images": [
        "static/description/work.png",
    ],
    # any module necessary for this one to work correctly
    "depends": ["base", "web", "mail", "point_of_sale"],
    "installable": True,
    # "cloc_exclude": [
    #     "static/src/libs/**/*",  # exclude a single folder
    # ],
    # always loaded
    "data": [
        "index.xml",
    ],
    "assets": {
        "point_of_sale.pos_assets_backend": [
            ("prepend", "pos_chat_button/static/src/js/ChatButton.js"),
            # ("prepend", 'pos_chat_button/static/src/js/messaging_notification_handler.js'),
            ("prepend", "pos_chat_button/static/src/js/main.js"),
        ],
        "point_of_sale.assets": [
            "pos_chat_button/static/src/css/**/*.css",
            "pos_chat_button/static/src/css/chat.css",
            # ANALOGY
            # ('include', 'mail.assets_discuss_public'),
            # ('remove', 'web/static/src/legacy/scss/import_bootstrap.scss'),
            # SCSS dependencies (the order is important)
            ("include", "web._assets_helpers"),
            # 'web/static/src/legacy/scss/bootstrap_overridden_report.scss',
            "web/static/lib/bootstrap/scss/_variables.scss",
            # redefine in css
            # 'web/static/src/legacy/scss/import_bootstrap.scss',
            # 'web/static/src/legacy/scss/bootstrap_review.scss',
            # 'web/static/src/core/utils/transitions.scss',
            # 'web/static/src/legacy/scss/bootstrap_overridden.scss',
            # 'web/static/src/webclient/webclient.scss',
            # 'web/static/src/webclient/webclient_extra.scss',
            # 'web/static/src/core/utils/*.scss',
        ],
        "web.assets_qweb": [
            "pos_chat_button/static/src/xml/**/*.xml",
        ],
    },
}
