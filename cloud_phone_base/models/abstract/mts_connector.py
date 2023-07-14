import json
import logging
import pytz
import requests
from datetime import datetime, timedelta
from requests.auth import HTTPBasicAuth
from requests.exceptions import Timeout

from odoo import fields, models
from odoo.exceptions import ValidationError


_logger = logging.getLogger(__name__)


class CloudPhoneConnectorMts(models.AbstractModel):
    _name = "cloud.phone.connector.factory.mts"
    _inherit = "cloud.phone.connector.factory"

    def _auth_request(self, connector_id, path, binary_content=False):
        try:
            response = requests.get(
                connector_id.url + path,
                auth=HTTPBasicAuth(connector_id.login, connector_id.password),
            )
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

    def _get_and_update_numbers(self, connector_id):
        """
        Create or update numbers
        Return set or numbers
        """
        path = "/numbers"
        numbers = self._auth_request(connector_id, path)
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
                connector_id=connector_id.id,
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

    def _get_record_mp3_attachment(
        self, connector_id, number, file_name, call_id
    ):
        path = "/file/{number}/{file_name}".format(
            number=number, file_name=file_name, external_id=call_id.external_id
        )
        attachment_raw = self._auth_request(
            connector_id,
            path,
            binary_content=True,
        )
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

    def _create_attachment(self, connector_id, call_id):
        attachment_mp3 = self._get_record_mp3_attachment(
            connector_id,
            call_id.number_id.tel,
            call_id.filename or call_id.external_id,
            call_id,
        )
        if attachment_mp3:
            attachment_id = self.env["ir.attachment"].create(attachment_mp3)
            call_id.ir_attachment_id = attachment_id
        else:
            attachment_mp3 = self._get_record_mp3_attachment(
                connector_id,
                call_id.tel,
                call_id.filename or call_id.external_id,
                call_id,
            )
            if attachment_mp3:
                attachment_id = self.env["ir.attachment"].create(attachment_mp3)
                call_id.ir_attachment_id = attachment_id

    def _get_and_update_call(self, connector_id, call, number):
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
            connector_id=connector_id.id,
            filename=call["FileName"],
        )

        if not call_id:
            call_id = self.env["cloud.phone.call"].create(call_data)
            # attach mp3 recording of call, if recDuration exist
            if call["RecDuration"] != "00:00:00":
                self._create_attachment(connector_id, call_id)

        # if try get when calling run, can request recording again later
        elif call["RecDuration"] != "00:00:00" and not call_id.ir_attachment_id:
            self._create_attachment(connector_id, call_id)

    def _get_and_update_calls(
        self, connector_id, begin_datetime, end_datetime, number
    ):
        path = f"/recs/{number.tel}/{begin_datetime}/{end_datetime}"
        _logger.info(f"Start update calls for number {number.id}")
        _logger.info(path)
        calls = self._auth_request(connector_id, path)
        _logger.info(f"Calls number: {len(calls)}")
        for call in calls:
            self._get_and_update_call(connector_id, call, number)

    def _update_numbers_and_fetch_calls(
        self, connector_id, days=None, minutes=60, wait_minutes=60
    ):
        numbers_ids = self._get_and_update_numbers(connector_id)
        for number in numbers_ids:
            delta = timedelta(days=days) if days else timedelta(minutes=minutes)
            waiting_time_end_call = timedelta(minutes=wait_minutes)
            # moscow time
            self._get_and_update_calls(
                connector_id,
                (
                    datetime.now(pytz.timezone("Europe/Moscow"))
                    - delta
                    - waiting_time_end_call
                ).strftime("%Y-%m-%dT%H:%M:%S"),
                (
                    datetime.now(pytz.timezone("Europe/Moscow"))
                    - waiting_time_end_call
                ).strftime("%Y-%m-%dT%H:%M:%S"),
                number,
            )
