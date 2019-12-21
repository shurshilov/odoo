# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
import json


class PosWebsiteSale(http.Controller):

    @http.route(['/map/config'], type='http', auth="public", website=True, methods=['POST','GET'], csrf=False)
    def map_config(self):
        lat = request.env['ir.config_parameter'].sudo().get_param("website_leaflet_lat")
        lng = request.env['ir.config_parameter'].sudo().get_param("website_leaflet_lng")
        enable = request.env['ir.config_parameter'].sudo().get_param("website_leaflet_enable")
        size = request.env['ir.config_parameter'].sudo().get_param("website_leaflet_size")
        return json.dumps({
            "lat":    lat,
            "lng":    lng,
            "enable": enable,
            "size":   size,
        })
