# -*- coding: utf-8 -*-
# Copyright 2020-2022 Artem Shurshilov
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
from odoo import fields, models


class Website(models.Model):
    _inherit = 'website'

    css_msg_in_stock = fields.Text("CSS style msg in stock",
                                   default="color: #fff;font-weight: 700;line-height: 18px;display: inline-block;padding: 3px 8px 4px;border-radius: 2px;background:green;padding10px")
    css_msg_out_stock = fields.Text("CSS style msg out stock",
                                    default="color: #fff;font-weight: 700;line-height: 18px;display: inline-block;padding: 3px 8px 4px;border-radius: 2px;background:red;padding10px")


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    css_msg_in_stock = fields.Text(
        related='website_id.css_msg_in_stock', readonly=False)
    css_msg_out_stock = fields.Text(
        related='website_id.css_msg_out_stock', readonly=False)
