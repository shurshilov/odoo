# -*- coding: utf-8 -*-
import pytz
from odoo import fields, models, api
from datetime import timedelta


class Number(models.Model):

    _inherit = "cloud.phone.number"

    mts_tz = fields.Char(string="Timezone -1 to 9")


class Connector(models.Model):

    _inherit = "cloud.phone.connector"

    cloud_phone_vendor = fields.Selection(
        selection_add=[("mts", "MTS")], ondelete={"mts": "cascade"}
    )

    @api.model
    def schedule_connector(
        self, days=None, minutes=60, wait_minutes=60, recreate=False
    ):
        super().schedule_connector(
            days=days, minutes=minutes, wait_minutes=wait_minutes, recreate=recreate
        )
        connector_ids = self.search(
            [("active", "=", True), ("cloud_phone_vendor", "=", "mts")]
        )
        for connector in connector_ids:
            numbers_ids = self.env["cloud.phone.connector.factory.mts"]._get_and_update_numbers(connector)
            for number in numbers_ids:
                delta = timedelta(days=days) if days else timedelta(minutes=minutes)
                waiting_time_end_call = timedelta(minutes=wait_minutes)
                self.env["cloud.phone.connector.factory.mts"]._get_and_update_calls(
                    connector,
                    # moscow time
                    (
                        fields.Datetime.now(pytz.timezone('Europe/Moscow'))
                        # + timedelta(hours=3)
                        - delta
                        - waiting_time_end_call
                    ).strftime("%Y-%m-%dT%H:%M:%S"),
                    (
                        fields.Datetime.now(pytz.timezone('Europe/Moscow'))
                        # + timedelta(hours=3)
                        - waiting_time_end_call
                    ).strftime("%Y-%m-%dT%H:%M:%S"),
                    number,
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
                    self.env["cloud.phone.connector.factory.mts"]._create_attachment(connector, call_id)