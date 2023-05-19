# -*- coding: utf-8 -*-
from odoo import fields, models


class Number(models.Model):

    _inherit = "cloud.phone.number"

    extension = fields.Char(string="Extension")
    comment = fields.Char(string="Comment")
    schema_name = fields.Char(string="Schema name")
    protocol = fields.Char(string="Protocol")


class Connector(models.Model):
    """Mango connector

    Arguments:
        url --  https://app.mango-office.ru/vpbx
    """

    _inherit = "cloud.phone.connector"

    vpbx_api_key = fields.Char(string="API key")
    vpbx_api_salt = fields.Char(string="Sign key")
    balance = fields.Float(string="Balance")
    cloud_phone_vendor = fields.Selection(
        selection_add=[("mango", "MANGO")], ondelete={"mango": "cascade"}
    )
