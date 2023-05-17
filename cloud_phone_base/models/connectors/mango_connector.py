# -*- coding: utf-8 -*-
from odoo import fields, models, api
from datetime import datetime
from datetime import timedelta


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

    @api.model
    def schedule_connector(
        self, days=None, minutes=60, wait_minutes=60, recreate=False
    ):
        super().schedule_connector(
            days=days, minutes=minutes, wait_minutes=wait_minutes, recreate=recreate
        )
        connector_ids = self.search(
            [("active", "=", True), ("cloud_phone_vendor", "=", "mango")]
        )
        for connector in connector_ids:
            # обновление списка подключенных номеров
            self.env["cloud.phone.connector.factory.mango"]._get_and_update_numbers(connector)
            # self._get_and_update_numbers2(connector)

            # обновление или добавление звонков и записей звонков, за период
            delta = timedelta(days=days) if days else timedelta(minutes=minutes)
            waiting_time_end_call = timedelta(minutes=wait_minutes)
            self.env["cloud.phone.connector.factory.mango"]._get_and_update_calls(
                connector,
                # moscow time
                int((
                    datetime.now()
                    # + timedelta(hours=3)
                    - delta
                    - waiting_time_end_call
                ).timestamp()),
                int((
                    datetime.now()
                    #  + timedelta(hours=3)
                      - waiting_time_end_call
                ).timestamp()),
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
                    self.env["cloud.phone.connector.factory.mango"]._create_attachment(connector, call_id)