from odoo import http
from odoo.http import request


class DomainVoip(http.Controller):
    @http.route(
        ["/domain/voip"], type="json", auth="user", methods=["POST"], csrf=False
    )
    def map_config(self):
        domain = (
            request.env["ir.config_parameter"]
            .sudo()
            .get_param("remote_desktop_voip_server")
        )
        return {
            "domain": domain,
        }
