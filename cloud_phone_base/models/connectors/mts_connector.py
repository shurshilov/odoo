# -*- coding: utf-8 -*-
from odoo import fields, models, api

from datetime import datetime
from datetime import timedelta
import logging
_logger = logging.getLogger(__name__)

class Number(models.Model):

    _inherit = "cloud.phone.number"

    mts_tz = fields.Char(string="Timezone -1 to 9")


class Connector(models.Model):

    _inherit = "cloud.phone.connector"

    cloud_phone_vendor = fields.Selection(
        selection_add=[("mts", "MTS")], ondelete={"mts": "cascade"}
    )

    def get_and_update_numbers(self):
        """
        Create or update numbers
        Return set or numbers
        """
        path = "/numbers"
        numbers = self._basic_auth_request(self.url + path)
        numbers_ids = self.env["cloud.phone.number"]
        for number in numbers:
            employee_id = self.find_by_number("hr.employee", number["Phone"])
            # partner_id = self.find_by_number("res.partner", number["Phone"])

            number_data = dict(
                tel=number["Phone"],
                recording_in=number["RecordIncomingCalls"],
                recording_out=number["RecordOutboundCalls"],
                employee_id=employee_id.id if employee_id else False,
                mts_tz=number["TimeZone"],
                connector_id=self.id,
                # partner_id=partner_id or False,
            )

            existed = self.env["cloud.phone.number"].search(
                [("tel", "=", number["Phone"])]
            )

            if existed:
                existed.write(number_data)
                numbers_ids += existed
            else:
                number_id = self.env["cloud.phone.number"].create(number_data)
                numbers_ids += number_id

        return numbers_ids

    def get_record_mp3_attachment(self, number, file_name, call_id):
        path = "/file/{number}/{file_name}".format(
            number=number, file_name=file_name, external_id=call_id.external_id
        )
        attachment_raw = self._basic_auth_request(self.url + path, binary_content=True)
        if not attachment_raw:
            return attachment_raw
        attachment = {
            "name": f"{path} {call_id.type} {''.join(i for i in call_id.number_id.tel if i.isdigit())} {call_id.tel}.mp3",
            "type": "binary",
            "res_id": call_id.id,
            "res_model": call_id._name,
            "raw": attachment_raw,
        }
        return attachment

    def create_attachment(self, call_id):
        attachment_mp3 = self.get_record_mp3_attachment(
            call_id.number_id.tel, call_id.filename or call_id.external_id, call_id
        )
        if attachment_mp3:
            attachment_id = self.env["ir.attachment"].create(attachment_mp3)
            call_id.ir_attachment_id = attachment_id
        else:
            attachment_mp3 = self.get_record_mp3_attachment(
                call_id.tel, call_id.filename or call_id.external_id, call_id
            )
            if attachment_mp3:
                attachment_id = self.env["ir.attachment"].create(attachment_mp3)
                call_id.ir_attachment_id = attachment_id

    def get_and_updete_call(self, call, number):
        """
        Get call from cloud or update if already exist
        update should when run when call already exist
        but not yet have recording
        """
        call_id = self.env["cloud.phone.call"].search(
            [("external_id", "=", call["Id"]), ("number_id.id", "=", number.id)]
        )
        call_data = dict(
            external_id=call["Id"],
            time=fields.Datetime.from_string(call["DateTime"].replace("T", " "))
            - timedelta(hours=3)
            + timedelta(hours=int(number.mts_tz)),
            number_id=number.id or False,
            type="incoming" if call["CallType"] == "incoming" else "outgoing",
            tel=call["Phone"],
            rec_duration=call["RecDuration"],
            call_duration=call["CallDuration"],
            connector_id=self.id,
            filename=call["FileName"],
        )

        if not call_id:
            call_id = self.env["cloud.phone.call"].create(call_data)
            # attach mp3 recording of call, if recDuration exist
            if call["RecDuration"] != "00:00:00":
                self.create_attachment(call_id)

        # if try get when calling run, can request recording again later
        elif call["RecDuration"] != "00:00:00" and not call_id.ir_attachment_id:
            self.create_attachment(call_id)

    def get_and_update_calls(self, number, begin_datetime, end_datetime):
        path = f"/recs/{number.tel}/{begin_datetime}/{end_datetime}"
        _logger.info(f"Start update calls for number {number.id}")
        _logger.info(path)
        calls = self._basic_auth_request(self.url + path)
        _logger.info(f"Calls number: {len(calls)}")
        for call in calls:
            self.get_and_updete_call(call, number)

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
            numbers_ids = connector.get_and_update_numbers()
            for number in numbers_ids:
                delta = timedelta(days=days) if days else timedelta(minutes=minutes)
                waiting_time_end_call = timedelta(minutes=wait_minutes)
                connector.get_and_update_calls(
                    number,
                    # moscow time
                    (
                        fields.Datetime.now()
                        + timedelta(hours=3)
                        - delta
                        - waiting_time_end_call
                    ).strftime("%Y-%m-%dT%H:%M:%S"),
                    (
                        fields.Datetime.now()
                        + timedelta(hours=3)
                        - waiting_time_end_call
                    ).strftime("%Y-%m-%dT%H:%M:%S"),
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
                    connector.create_attachment(call_id)
