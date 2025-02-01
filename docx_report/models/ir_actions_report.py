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

from odoo import api, fields, models

# from mailmerge import MailMerge
from . import mailmerge


class IrActionsReport(models.Model):
    _inherit = "ir.actions.report"

    report_type = fields.Selection(selection_add=[("docx", "DOCX")])
    template_docx = fields.Binary(string="Docx template", attachment=True)

    def get_orm_from_string(self, record, string):
        list_field = string.split(".")
        res = record
        for myfield in list_field:
            res = res[myfield]
            # for name, field in res[myfield]._fields.iteritems():
            # for name, field in res[myfield]._fields.items():
            #     if field == myfield and not isinstance(field, (fields.Many2many, fields.One2many)):
            #         res = res[myfield]
            #     else:
            #         if field == myfield:
            #             for i in res[myfield]:
            #                 j = list_field.index(myfield)
            #                 string1= ".".join(list_field[:j+1])
            #                 res += self.get_orm_from_string(self, i, string1)
        return res

    @api.model
    def render_docx(self, docids, data=None):
        if not data:
            data = {}
        data.setdefault("report_type", "docx")
        data = self._get_rendering_context(docids, data)
        # READ DATA
        content = base64.b64decode(self.template_docx)
        document_1 = mailmerge.MailMerge(io.BytesIO(content))

        # MERGE DATA
        document_1.get_merge_fields()
        docx_list_text = document_1.get_merge_fields_text()
        docx_dict = {}
        # mystr =""
        for key in docx_list_text:
            for doc in data["docs"]:
                # docx_dict.update({key:doc[key]})
                # docx_dict.update({key:self.get_orm_from_string(doc,key)})
                # mystr +=key['text_origin']+"|" +key['text']+"\n"
                if key["text"][0] == '"':
                    try:
                        docx_dict.update({key["text_origin"]: str(eval(eval(key["text"])))})
                    except:
                        docx_dict.update({key["text_origin"]: str(eval(key["text"]))})
                else:
                    docx_dict.update({key["text_origin"]: str(eval(key["text"]))})
        # raise UserError(mystr)
        document_1.merge(**docx_dict)

        # WRITE DATA
        myio = io.BytesIO()
        document_1.write(myio)
        myio.getvalue()

        return myio.getvalue(), "docx"
