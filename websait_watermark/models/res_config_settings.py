# -*- coding: utf-8 -*-
# Copyright 2019 Artem Shurshilov
# License OPL-1.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models
from PIL import Image
import io
import base64
from odoo import http
from odoo.http import request
import odoo.addons.web.controllers.main as main


class Extension(main.Binary):

    @http.route(['/web/image',
                 '/web/image/<string:xmlid>',
                 '/web/image/<string:xmlid>/<string:filename>',
                 '/web/image/<string:xmlid>/<int:width>x<int:height>',
                 '/web/image/<string:xmlid>/<int:width>x<int:height>/<string:filename>',
                 '/web/image/<string:model>/<int:id>/<string:field>',
                 '/web/image/<string:model>/<int:id>/<string:field>/<string:filename>',
                 '/web/image/<string:model>/<int:id>/<string:field>/<int:width>x<int:height>',
                 '/web/image/<string:model>/<int:id>/<string:field>/<int:width>x<int:height>/<string:filename>',
                 '/web/image/<int:id>',
                 '/web/image/<int:id>/<string:filename>',
                 '/web/image/<int:id>/<int:width>x<int:height>',
                 '/web/image/<int:id>/<int:width>x<int:height>/<string:filename>',
                 '/web/image/<int:id>-<string:unique>',
                 '/web/image/<int:id>-<string:unique>/<string:filename>',
                 '/web/image/<int:id>-<string:unique>/<int:width>x<int:height>',
                 '/web/image/<int:id>-<string:unique>/<int:width>x<int:height>/<string:filename>'], type='http', auth="public")
    def content_image(self, xmlid=None, model='ir.attachment', id=None, field='datas',
                      filename_field='datas_fname', unique=None, filename=None, mimetype=None,
                      download=None, width=0, height=0, crop=False, related_id=None, access_mode=None,
                      access_token=None, avoid_if_small=False, upper_limit=False, signature=False):
        if field == 'image' and (model == 'product.template' or model == 'product.product'):
            if request.env['ir.config_parameter'].sudo().get_param("website_watermark_enable"):
                if model == 'product.template':
                    field = 'watermark_image'
                else:
                    field = 'watermark_image_product'
        return super(Extension, self).content_image(xmlid, model, id, field,
                                                    filename_field, unique, filename, mimetype,
                                                    download, width, height, crop, related_id, access_mode,
                                                    access_token, avoid_if_small, upper_limit, signature)

class ProductProduct(models.Model):
    _name = 'product.product'
    _inherit = 'product.product'

    watermark_image_product = fields.Binary('Image with watermark product')

class Product(models.Model):
    _name = 'product.template'
    _inherit = 'product.template'

    watermark_image = fields.Binary('Image with watermark')


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    @api.model
    def get_default_website_watermark_enable(self):
        website_watermark_enable = self.env['ir.config_parameter'].get_param("website_watermark_enable")
        return website_watermark_enable

    @api.model
    def get_default_website_watermark_image(self):
        website_watermark_image = self.env['ir.config_parameter'].get_param("website_watermark_image")
        return website_watermark_image

    @api.model
    def get_default_website_watermark_centr(self):
        website_watermark_centr = self.env['ir.config_parameter'].get_param("website_watermark_centr")
        return website_watermark_centr

    @api.model
    def get_default_website_watermark_transparent(self):
        website_watermark_transparent = self.env['ir.config_parameter'].get_param("website_watermark_transparent")
        if website_watermark_transparent:
            return website_watermark_transparent
        else:
            return 0

    website_watermark_image = fields.Binary('Image for watermark', default=get_default_website_watermark_image)
    website_watermark_text = fields.Char('Text for watermark, image will default')
    website_watermark_enable = fields.Boolean("Enable/Disable website watermark", default=get_default_website_watermark_enable)
    website_watermark_centralize = fields.Boolean("centralize watermark or leave in the upper left corner", default=get_default_website_watermark_centr)
    website_watermark_transparent = fields.Integer("transparent watermark 0-256 opacity,0 - disable", default=get_default_website_watermark_transparent)
    website_watermark_mode = fields.Selection([
        ('text', 'Watermark just text'),
        ('image', 'Watermark your own image'),
    ], string='Selection mode', default='image')

    @api.multi
    def set_website_watermark(self):
        config_parameters = self.env['ir.config_parameter']
        config_parameters.set_param("website_watermark_enable", self.website_watermark_enable)
        config_parameters.set_param("website_watermark_image", self.website_watermark_image)
        config_parameters.set_param("website_watermark_centr", self.website_watermark_centralize)
        config_parameters.set_param("website_watermark_transparent", self.website_watermark_transparent)

    @api.multi
    def write(self, values):
        result = super(ResConfigSettings, self).write(values)
        self.set_website_watermark()
        if self.website_watermark_image and self.website_watermark_enable:
            watermark = Image.open(io.BytesIO(base64.b64decode(self.website_watermark_image))).convert("RGBA")
            if self.website_watermark_transparent and self.website_watermark_transparent < 256 and self.website_watermark_transparent >0:
                watermark.putalpha(self.website_watermark_transparent)
            for prod in self.env['product.template'].search([],order="write_date",limit=250):
                if prod.image:
                    img = Image.open(io.BytesIO(base64.b64decode(prod.image))).convert("RGBA")
                    #x, y = watermark.size
                    x = int((img.size[0] / 2) - (watermark.size[0] / 2))
                    y = int((img.size[1] / 2) - (watermark.size[1] / 2))
                    #img.paste(watermark, (0, 0, x, y), watermark)
                    width, height = img.size
                    #transparent = Image.new('RGBA', (width, height), (0,0,0,0))
                    #transparent.paste(img, (0,0))
                    if self.website_watermark_centralize:
                        #transparent.paste(watermark, (x, y), mask=watermark)
                        img.paste(watermark, (x, y), watermark)
                    else:
                        #transparent.paste(watermark, (0, 0, x, y), mask=watermark)
                        img.paste(watermark, (0, 0, x, y), watermark)
                    #transparent.show()
                    with io.BytesIO() as output:
                        img.save(output, format=img.format) if img.format else img.save(output, format='PNG')
                        #transparent.save(output)
                        prod.watermark_image = base64.b64encode(output.getvalue())
            for prod in self.env['product.product'].search([],order="write_date",limit=250):
                if prod.image:
                    img = Image.open(io.BytesIO(base64.b64decode(prod.image))).convert("RGBA")
                    #x, y = watermark.size
                    x = int((img.size[0] / 2) - (watermark.size[0] / 2))
                    y = int((img.size[1] / 2) - (watermark.size[1] / 2))
                    #img.paste(watermark, (0, 0, x, y), watermark)
                    width, height = img.size
                    #transparent = Image.new('RGBA', (width, height), (0,0,0,0))
                    #transparent.paste(img, (0,0))
                    if self.website_watermark_centralize:
                        #transparent.paste(watermark, (x, y), mask=watermark)
                        img.paste(watermark, (x, y), watermark)
                    else:
                        #transparent.paste(watermark, (0, 0, x, y), mask=watermark)
                        img.paste(watermark, (0, 0, x, y), watermark)
                    #transparent.show()
                    with io.BytesIO() as output:
                        img.save(output, format=img.format) if img.format else img.save(output, format='PNG')
                        #transparent.save(output)
                        prod.watermark_image_product = base64.b64encode(output.getvalue())
        return result
