# Copyright 2021 Artem Shurshilov
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

# from odoo.addons.web.controllers.main import ReportController


class IrActionsReport(models.Model):
    _inherit = "ir.actions.report"

    portal_bisible = fields.Boolean("Portal visible", default=True)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def get_portal_url_multi(
        self, report_name, report_type, report_id, download=False
    ):
        self.ensure_one()
        url = "/report/download/public" + "?access_token=%s%s%s%s%s%s" % (
            self._portal_ensure_token(),
            "&order_id=%s" % self.id if self.id else "",
            "&report_ref=%s" % report_name if report_name else "",
            "&report_type=%s" % report_type if report_type else "",
            "&report_id=%s" % report_id if report_id else "",
            "&download=true" if download else "",
        )
        return url
