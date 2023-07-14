# Copyright 2020 Artem Shurshilov
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
from odoo.addons.base.models import ir_property

ir_property.TYPE2FIELD = {
    "char": "value_text",
    "float": "value_float",
    "boolean": "value_integer",
    "integer": "value_integer",
    "text": "value_text",
    "html": "value_text",
    "binary": "value_binary",
    "many2one": "value_reference",
    "date": "value_datetime",
    "datetime": "value_datetime",
    "selection": "value_text",
}
ir_property.TYPE2CLEAN = {
    "boolean": bool,
    "integer": lambda val: val or False,
    "float": lambda val: val or False,
    "char": lambda val: val or False,
    "text": lambda val: val or False,
    "html": lambda val: val or False,
    "selection": lambda val: val or False,
    "binary": lambda val: val or False,
    "date": lambda val: val.date() if val else False,
    "datetime": lambda val: val or False,
}


class Property(models.Model):
    _inherit = "ir.property"

    type = fields.Selection(
        selection_add=[("html", "Html")], ondelete={"html": "cascade"}
    )

    def get_by_record(self):
        if self.type in ("html"):
            return self.value_text
        return super().get_by_record()


class ResUsers(models.Model):
    _inherit = "res.users"

    signature = fields.Html(company_dependent=True)


class ResPartners(models.Model):
    _inherit = "res.partner"

    email = fields.Char(company_dependent=True)
