# -*- coding: utf-8 -*-

from odoo import models, api
from odoo.http import request


class IrUiView(models.Model):
	_inherit = 'ir.ui.view'

	@api.model
	def _render_template(self, template, values=None, engine='ir.qweb'):
		res = super()._render_template(template, values, engine)
		try:
			website = request.website
		except:
			website = False
		website_watermark_enable = website and website.website_watermark_enable or False
		request.session['website_watermark_enable'] = False
		if website_watermark_enable and values:
				request.session['website_watermark_enable'] = website.website_watermark_enable
		return res
