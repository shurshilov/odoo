# Copyright 2019 Artem Shurshilov
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

import json

from odoo import http


class IapFirebase(http.Controller):
    # @http.route('/iap_firebase_key', auth='user', type="json", cors='*')
    # def index(self, **kw):
    #     res = {}
    #     firebase_key = request.env['ir.config_parameter'].sudo().get_param('firebase_key')
    #     res.update({'firebase_key': True if firebase_key else False})
    #     return res

    @http.route(
        ["/iap/firebase"],
        type="http",
        auth="public",
        methods=["POST", "GET"],
        csrf=False,
    )
    def map_config(self):
        return json.dumps({"enable": True})
