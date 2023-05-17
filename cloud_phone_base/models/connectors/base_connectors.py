# -*- coding: utf-8 -*-
from odoo import fields, models, api


class Connector(models.Model):

    _name = "cloud.phone.connector"
    _description = "cloud.phone.connector"

    cloud_phone_vendor = fields.Selection(
        [("default", "Default")],
        required=True,
        default="default",
    )
    name = fields.Char(string="Name")
    active = fields.Boolean(string="Active", default=False)
    url = fields.Char(string="Url")
    login = fields.Char(string="Login")
    password = fields.Char(string="Password")
    company_id = fields.Many2one("res.company", string="Company")

   # THIS SHOULD USE AS ABSTRACT FABRIC 
    @api.model
    def schedule_connector(
        self, days=None, minutes=60, wait_minutes=60, recreate=False
    ):
        pass