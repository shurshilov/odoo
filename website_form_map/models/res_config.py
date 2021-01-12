# -*- coding: utf-8 -*-
# Copyright 2019 Shurshilov Artem
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    @api.model
    def get_default_website_leaflet_enable(self):
        return self.env['ir.config_parameter'].get_param("website_leaflet_enable")

    @api.model
    def get_default_website_leaflet_lat(self):
        return self.env['ir.config_parameter'].get_param("website_leaflet_lat")

    @api.model
    def get_default_website_leaflet_lng(self):
        return self.env['ir.config_parameter'].get_param("website_leaflet_lng")

    @api.model
    def get_default_website_leaflet_size(self):
        return self.env['ir.config_parameter'].get_param("website_leaflet_size")

    website_leaflet_lat = fields.Float('Coord latitude', default=get_default_website_leaflet_lat)
    website_leaflet_lng = fields.Float('Coord longitude', default=get_default_website_leaflet_lng)
    website_leaflet_enable = fields.Boolean("Enable/Disable leaflet", default=get_default_website_leaflet_enable)
    website_leaflet_size = fields.Integer("Size of map(230 - norm)", default=get_default_website_leaflet_size)

    def set_website_leaflet(self):
        config_parameters = self.env['ir.config_parameter']
        config_parameters.set_param("website_leaflet_lat", self.website_leaflet_lat)
        config_parameters.set_param("website_leaflet_lng", self.website_leaflet_lng)
        config_parameters.set_param("website_leaflet_enable", self.website_leaflet_enable)
        config_parameters.set_param("website_leaflet_size", self.website_leaflet_size)

    def write(self, values):
        result = super(ResConfigSettings, self).write(values)
        self.set_website_leaflet()
        return result