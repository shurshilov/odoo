# Copyright (C) 2020 Artem Shurshilov <shurshilov.a@yandex.ru>
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
    "name": "Odoo cloud companion",
    "summary": """
		Google Drive, Microsoft OneDrive, Dropbox Clouds Odoo Integrations
        """,
    "author": "EURO ODOO, Shurshilov Artem",
    "website": "https://eurodoo.com",
    "live_test_url": "https://eurodoo.com/login_employee?login=demo1&password=demo777",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Point Of Sale",
    "version": "13.5.10",
    "license": "OPL-1",
    "price": 4,
    "currency": "EUR",
    "images": [
        "static/description/companion.png",
        "static/description/button_url.png",
        "static/description/button_manage_search.png",
        "static/description/button_download.png",
    ],
    # any module necessary for this one to work correctly
    "depends": [
        "base",
        "web",
        "mail",
        "dropbox_picker",
        "google_drive_picker",
        "microsoft_onedrive_picker",
        "attachments_manager",
    ],
    "installable": False,
    # always loaded
    "data": [
        #'views/assets.xml',
        #'views/document_url_view.xml',
        #'security/restrict_manage_attachments_security.xml',
    ],
    "qweb": [
        #'static/src/xml/pos.xml',
    ],
}
