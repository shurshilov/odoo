# -*- coding: utf-8 -*-
from odoo import fields, models, api
from odoo.exceptions import ValidationError

import requests
from requests.auth import HTTPBasicAuth
from requests.exceptions import Timeout
import json


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

    def _basic_auth_request(self, url, binary_content=False):
        try:
            response = requests.get(url, auth=HTTPBasicAuth(self.login, self.password))
            if response.status_code == 404:
                return {}
            if binary_content:
                return response.content
            else:
                return json.loads(response.text)
        except Timeout as e:
            raise ValidationError("Request timeout error " + str(e))
        except Exception as e:
            raise ValidationError("Request unknown error " + str(e))

    @staticmethod
    def swipe(str1, str2):
        if str1 in str2:
            return True
        if str2 in str1:
            return True
        return False

    def find_by_number(self, model, number):
        for rec in self.env[model].search([]):
            if rec.work_phone:
                work_phone_digits = "".join(i for i in rec.work_phone if i.isdigit())
                if work_phone_digits:
                    if self.swipe(work_phone_digits, number):
                        return rec
                    if self.swipe(work_phone_digits[1:], number):
                        return rec

            if rec.mobile_phone:
                mobile_phone_digits = "".join(
                    i for i in rec.mobile_phone if i.isdigit()
                )
                if mobile_phone_digits:
                    if self.swipe(mobile_phone_digits, number):
                        return rec
                    if self.swipe(mobile_phone_digits[1:], number):
                        return rec

    @api.model
    def schedule_connector(
        self, days=None, minutes=60, wait_minutes=60, recreate=False
    ):
        pass
