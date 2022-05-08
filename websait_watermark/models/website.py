# -*- coding: utf-8 -*-
# Copyright 2019-2022 Shurshilov Artem

from odoo import api, fields, models
from PIL import Image
import io
import base64
from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.main import Binary


class BinaryWatermark(Binary):
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
                      filename_field='name', unique=None, filename=None, mimetype=None,
                      download=None, width=0, height=0, crop=False, access_token=None,
                      **kwargs):
        if request and request.session.get('website_watermark_enable', False):
            if (model == 'product.template' or model == 'product.product') and \
                field == 'image_1920' or field == 'image_1024' or field == 'image_512' or field == 'image_256' or field == 'image_128' or field == 'image_64':
                    if model == 'product.template':
                        field = 'watermark_image'
                    else:
                        field = 'watermark_image_product'
        # other kwargs are ignored on purpose
        res = super().content_image(xmlid=xmlid, model=model, id=id, field=field,
                                    filename_field=filename_field, unique=unique, filename=filename, mimetype=mimetype,
                                    download=download, width=width, height=height, crop=crop, access_token=access_token,
                                    **kwargs)
        return res


class ProductProduct(models.Model):
    _name = 'product.product'
    _inherit = 'product.product'

    watermark_image_product = fields.Image('Image with watermark product')


class Product(models.Model):
    _name = 'product.template'
    _inherit = 'product.template'

    watermark_image = fields.Image('Image with watermark')

class Website(models.Model):

    _inherit = "website"
    _description = "Website"

    website_watermark_image = fields.Binary(
        'Image for watermark')
    website_watermark_text = fields.Char(
        'Text for watermark, image will default')
    website_watermark_enable = fields.Boolean(
        "Enable/Disable website watermark", default=False)
    website_watermark_centralize = fields.Boolean(
        "centralize watermark or leave in the upper left corner", default=True)
    website_watermark_transparent = fields.Integer(
        "transparent watermark 0-256 opacity,0 - disable", default=0)
    website_watermark_mode = fields.Selection([
        ('text', 'Watermark just text'),
        ('image', 'Watermark your own image'),
    ], string='Selection mode', default='image')

    def write(self, values):
        result = super().write(values)
        if self.website_watermark_image and self.website_watermark_enable:
            watermark = Image.open(io.BytesIO(base64.b64decode(self.website_watermark_image))).convert("RGBA")

            if self.website_watermark_transparent and self.website_watermark_transparent < 256 and self.website_watermark_transparent > 0:
                watermark.putalpha(self.website_watermark_transparent)

            for prod in self.env['product.template'].search([]):
                if prod.image_1920:
                    img = Image.open(io.BytesIO(base64.b64decode(prod.image_1920))).convert("RGBA")
                    x = int((img.size[0] / 2) - (watermark.size[0] / 2))
                    y = int((img.size[1] / 2) - (watermark.size[1] / 2))

                    if self.website_watermark_centralize:
                        img.paste(watermark, (x, y), watermark)
                    else:
                        img.paste(watermark, (0, 0, x, y), watermark)

                    with io.BytesIO() as output:
                        img.save(output, format=img.format) if img.format else img.save(output, format='PNG')
                        prod.watermark_image = base64.b64encode(output.getvalue())

            for prod in self.env['product.product'].search([]):
                if prod.image_1920:
                    img = Image.open(io.BytesIO(base64.b64decode(prod.image_1920))).convert("RGBA")
                    x = int((img.size[0] / 2) - (watermark.size[0] / 2))
                    y = int((img.size[1] / 2) - (watermark.size[1] / 2))
                    if self.website_watermark_centralize:
                        img.paste(watermark, (x, y), watermark)
                    else:
                        img.paste(watermark, (0, 0, x, y), watermark)
                    with io.BytesIO() as output:
                        img.save(output, format=img.format) if img.format else img.save(output, format='PNG')
                        prod.watermark_image_product = base64.b64encode(output.getvalue())
        return result
