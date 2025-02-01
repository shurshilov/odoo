from odoo import api, models
from odoo.http import request


class IrUiView(models.Model):
    _inherit = "ir.ui.view"

    @api.model
    def _render_template(self, template, values=None):
        res = super()._render_template(template, values)
        try:
            website = request.website
        except:
            website = False
        webp_enable = website and website.webp_enable or False
        request.session["webp_enable"] = False
        if webp_enable and values:
            request.session["webp_quality"] = website.webp_quality
            request.session["webp_enable"] = website.webp_enable
        return res
