# -*- coding: utf-8 -*-
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

# from odoo import http
# from odoo.http import request
# import requests
# try:
#     # Python 3
#     from urllib.parse import urlparse
# except:
#     from urlparse import urlparse
# try:
#     from BytesIO import BytesIO
# except ImportError:
#     from io import BytesIO


# class SynologyPicker(http.Controller):
#     @http.route(['/synology/preview', ], type='http', auth='public')
#     def download_attachment(self, attachment_id):
#         # Check if this is a valid attachment id
#         if not attachment_id:
#             return request.not_found()
#         attachment = request.env['ir.attachment'].sudo().search([('id', '=', int(attachment_id))])

#         url = urlparse(attachment["url"])
#         file = requests.get(url.geturl(), verify=False)
#         if not file:
#             return request.not_found()
#         data = BytesIO(file.content)
#         return http.send_file(data, filename=attachment['name'], as_attachment=False)
