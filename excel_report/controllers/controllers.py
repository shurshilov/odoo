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

from odoo import http
from odoo.http import content_disposition, request
from odoo.tools.safe_eval import safe_eval, time
from werkzeug.urls import url_decode
from odoo.addons.web.controllers.main import ReportController
import json


class ReportControllerExcel(ReportController):
    @http.route(
        [
            "/report/<converter>/<reportname>",
            "/report/<converter>/<reportname>/<docids>",
        ],
        type="http",
        auth="user",
        website=True,
    )
    def report_routes(self, reportname, docids=None, converter=None, **data):
        report = request.env["ir.actions.report"]._get_report_from_name(
            reportname
        )
        context = dict(request.env.context)
        new_data = dict(data)

        if docids:
            docids_list = [int(i) for i in docids.split(",")]
        if new_data.get("options"):
            new_data.update(json.loads(new_data.pop("options")))
        if new_data.get("context"):
            # Ignore 'lang' here, because the context in data is the one from the webclient *but* if
            # the user explicitely wants to change the lang, this mechanism overwrites it.
            new_data["context"] = json.loads(new_data["context"])
            if new_data["context"].get("lang"):
                del new_data["context"]["lang"]
            context.update(new_data["context"])
        if converter == "excel":
            text, type = report.with_context(context).render_excel(
                docids_list, data=new_data
            )
            texthttpheaders = [
                ("Content-Type", "text/plain"),
                ("Content-Length", len(text)),
            ]
            if type == "pdf":
                texthttpheaders = [
                    ("Content-Type", "application/pdf"),
                    ("Content-Length", len(text)),
                ]
            return request.make_response(text, headers=texthttpheaders)
        res = super().report_routes(reportname, docids, converter, **data)
        return res

    @http.route(["/report/download"], type="http", auth="user")
    def report_download(self, data, token, context=None):
        """This function is used by 'action_manager_report.js' in order to trigger the download of
        a pdf/controller report.

        :param data: a javascript array JSON.stringified containg report internal url ([0]) and
        type [1]
        :returns: Response with a filetoken cookie and an attachment header
        """
        requestcontent = json.loads(data)
        url, type = requestcontent[0], requestcontent[1]
        # raise UserError(type)
        if type in ["qweb-excel"]:
            # raise UserError(type)
            converter = "excel"  # if type == 'qweb-pdf' else 'text'
            extension = "xlsx"  # if type == 'qweb-pdf' else 'txt'
            pattern = (
                "/report/excel/"  # if type == 'qweb-pdf' else '/report/text/'
            )
            reportname = url.split(pattern)[1].split("?")[0]

            docids = None
            if "/" in reportname:
                reportname, docids = reportname.split("/")

            if docids:
                # Generic report:
                response = self.report_routes(
                    reportname,
                    docids=docids,
                    converter=converter,
                    context=context,
                )
            else:
                # Particular report:
                data = dict(
                    url_decode(url.split("?")[1]).items()
                )  # decoding the args represented in JSON
                if "context" in data:
                    context, data_context = json.loads(
                        context or "{}"
                    ), json.loads(data.pop("context"))
                    context = json.dumps({**context, **data_context})
                response = self.report_routes(
                    reportname, converter=converter, context=context, **data
                )

            report = request.env["ir.actions.report"]._get_report_from_name(
                reportname
            )
            if report.excel_out_report_type != "excel":
                extension = report.excel_out_report_type
            filename = "%s.%s" % (report.name, extension)

            if docids:
                ids = [int(x) for x in docids.split(",")]
                obj = request.env[report.model].browse(ids)
                if report.print_report_name and not len(obj) > 1:
                    report_name = safe_eval(
                        report.print_report_name, {"object": obj, "time": time}
                    )
                    filename = "%s.%s" % (report_name, extension)
            response.headers.add(
                "Content-Disposition", content_disposition(filename)
            )
            response.set_cookie("fileToken", token)
            return response
        res = super().report_download(data, token, context)
        return res
