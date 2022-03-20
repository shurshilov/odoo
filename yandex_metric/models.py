# -*- coding: utf-8 -*-

from odoo import fields, api, models


class ResConfigSettingsYandex(models.TransientModel):
    _inherit = 'res.config.settings'

    yandex_metric = fields.Text(string='Yandex metrica code', help="Set your personal yandex metrica code from yandex")

    def set_values(self):
        res = super(ResConfigSettingsYandex, self).set_values()
        config_parameters = self.env['ir.config_parameter']
        config_parameters.set_param("yandex_metric", self.yandex_metric)
        return res

    @api.model
    def get_values(self):
        res = super(ResConfigSettingsYandex, self).get_values()
        res.update(yandex_metric = self.env['ir.config_parameter'].get_param('yandex_metric'))
        return res
