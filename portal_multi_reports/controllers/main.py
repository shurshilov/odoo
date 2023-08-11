######################################################################################################
#
# Copyright (C) B.H.C. sprl - All Rights Reserved, http://www.bhc.be
# Copyright (c) 2020 Shurshilov Artem (shurshilov.a@yandex.ru)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied,
# including but not limited to the implied warranties
# of merchantability and/or fitness for a particular purpose
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>
######################################################################################################
from odoo import http, SUPERUSER_ID
from odoo.exceptions import AccessError, MissingError
from odoo.addons.sale.controllers.portal import CustomerPortal
from odoo.http import request, content_disposition


class CustomerPortal(CustomerPortal):
    @http.route(
        ["/report/download/public"], type="http", auth="public", website=True
    )
    def show_report_by_id(
        self, access_token, order_id, report_type, report_id, download=False
    ):
        order_id = int(order_id)
        report_id = int(report_id)
        try:
            order_sudo = self._document_check_access(
                "sale.order", order_id, access_token=access_token
            )
        except (AccessError, MissingError):
            return request.redirect("/my")

        report_sudo = (
            order_sudo.env["ir.actions.report"]
            .browse(report_id)
            .with_user(SUPERUSER_ID)
        )

        method_name = "_render_%s" % (report_type)
        if report_type in ("qweb-text"):
            method_name = "_render_qweb_text"
        if report_type in ("qweb-html"):
            method_name = "_render_qweb_html"
        if report_type in ("qweb-pdf"):
            method_name = "_render_qweb_pdf"
        if report_type in ("docx"):
            method_name = "render_docx"
        if report_type in ("excel"):
            method_name = "render_excel"

        text, type = getattr(report_sudo, method_name)(
            [order_id], data={"report_type": report_type}
        )
        texthttpheaders = [
            ("Content-Type", "text/plain"),
            ("Content-Length", len(text)),
        ]
        extension = "txt"

        if report_type == "qweb-pdf" or type == "pdf":
            texthttpheaders = [
                ("Content-Type", "application/pdf"),
                ("Content-Length", len(text)),
            ]
            extension = "pdf"

        elif report_type == "docx":
            if report_sudo.out_report_type != "docx":
                extension = report_sudo.out_report_type
            else:
                texthttpheaders = [
                    (
                        "Content-Type",
                        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    ),
                    ("Content-Length", len(text)),
                ]
                extension = "docx"

        elif report_type == "excel":
            if report_sudo.excel_out_report_type != "excel":
                extension = report_sudo.excel_out_report_type
            else:
                texthttpheaders = [
                    ("Content-Type", "application/vnd.ms-excel"),
                    ("Content-Length", len(text)),
                ]
                extension = "xlsx"

        filename = "%s.%s" % (report_sudo.name, extension)
        if download:
            texthttpheaders.append(
                ("Content-Disposition", content_disposition(filename))
            )
        return request.make_response(text, headers=texthttpheaders)

    def _order_get_page_view_values(self, order, access_token, **kwargs):
        values = super()._order_get_page_view_values(
            order, access_token, **kwargs
        )
        values["available_reports"] = (
            order.env["ir.actions.report"]
            .search(
                [("portal_bisible", "=", True), ("model", "=", "sale.order")]
            )
            .with_user(SUPERUSER_ID)
        )
        return values
