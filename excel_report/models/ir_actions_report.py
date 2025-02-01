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

import base64
import io
from odoo import models, fields, api

# import openpyxl
from . import openpyxl
import re
import logging

_logger = logging.getLogger(__name__)


class IrActionsReport(models.Model):
    _inherit = "ir.actions.report"

    report_type = fields.Selection(selection_add=[("excel", "EXCEL")])
    template_excel = fields.Binary(string="Excel template", attachment=True)

    @api.model
    def render_excel(self, docids, data=None):
        if not data:
            data = {}
        data.setdefault("report_type", "excel")
        data = self._get_rendering_context(docids, data)
        # READ DATA
        content = base64.b64decode(self.template_excel)

        # MERGE DATA
        # open xcel sheets
        wb1 = openpyxl.load_workbook(io.BytesIO(content))
        ws1 = wb1.active

        # compare each element
        for doc in data["docs"]:
            for row in range(ws1.max_row):
                for column in range(ws1.max_column):
                    val = ws1.cell(row=row + 1, column=column + 1).value
                    if isinstance(val, str):
                        result = re.findall(r"(odoo\(.*?\))", val)
                        if len(result):
                            new_val = eval(result[0][5:-1])
                            if isinstance(new_val, float):
                                new_val = str(new_val).replace(".", ",")
                            else:
                                new_val = str(new_val)
                            ws1.cell(row=row + 1, column=column + 1).value = re.sub(
                                r"(odoo\(.*?\))", new_val, val
                            )

        # WRITE DATA
        myio = io.BytesIO()
        wb1.save(myio)
        myio.getvalue()

        return myio.getvalue(), "excel"
