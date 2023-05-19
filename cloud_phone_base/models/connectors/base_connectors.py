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

    @api.model
    def schedule_connector(
        self, days=None, minutes=60, wait_minutes=60, recreate=False
    ):
        connector_ids = self.search([("active", "=", True)])
        for connector in connector_ids:
            # ABSTRACT FABRIC
            self.env[
                "cloud.phone.connector.factory." + connector.cloud_phone_vendor
            ]._update_numbers_and_fetch_calls(
                connector, days=days, minutes=minutes, wait_minutes=wait_minutes
            )

            if recreate:
                without_recording_call_ids = self.env["cloud.phone.call"].search(
                    [
                        ("rec_duration", "!=", "00:00:00"),
                        ("ir_attachment_id", "=", False),
                        ("connector_id", "=", connector.id),
                    ]
                )
                for call_id in without_recording_call_ids:
                    self.env[
                        "cloud.phone.connector.factory" + connector.cloud_phone_vendor
                    ]._create_attachment(connector, call_id)
