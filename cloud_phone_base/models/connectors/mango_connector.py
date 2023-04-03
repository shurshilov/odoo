# -*- coding: utf-8 -*-
import time
from odoo import fields, models, api

import base64
from datetime import timedelta
from datetime import datetime

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

    def get_and_update_numbers_mango2(self):
        """
        Create or update numbers
        Return set or numbers
        """
        path = "/config/users/request"
        numbers = self._mango_auth_request(self.url + path)
        numbers_ids = self.env["cloud.phone.number"]
        # TODO: sometimes users not in numbers
        for user in numbers.get("users"):
            for number in user["telephony"]["numbers"]:
                employee_id = self.find_by_number("hr.employee", number["number"])

                number_data = dict(
                    tel=number["number"],
                    employee_id=employee_id.id if employee_id else False,
                    # comment=number["comment"],
                    # schema_name=number["schema_name"],
                    extension=user["telephony"]["extension"],
                    name=user["general"]["name"],
                    connector_id=self.id,
                    protocol=number["protocol"]
                )

                existed = self.env["cloud.phone.number"].search(
                    [("tel", "=", number["number"])]
                )

                if existed:
                    existed.write(number_data)
                    numbers_ids += existed
                else:
                    number_id = self.env["cloud.phone.number"].create(number_data)
                    numbers_ids += number_id

        return numbers_ids

    def get_and_update_numbers_mango(self):
        """
        Create or update numbers
        Return set or numbers
        """
        path = "/incominglines"
        numbers = self._mango_auth_request(self.url + path)
        numbers_ids = self.env["cloud.phone.number"]
        for number in numbers["lines"]:
            employee_id = self.find_by_number("hr.employee", number["number"])

            number_data = dict(
                tel=number["number"],
                employee_id=employee_id.id if employee_id else False,
                comment=number["comment"],
                schema_name=number["schema_name"],
                name=number["name"],
                connector_id=self.id,
            )

            existed = self.env["cloud.phone.number"].search(
                [("tel", "=", number["number"])]
            )

            if existed:
                existed.write(number_data)
                numbers_ids += existed
            else:
                number_id = self.env["cloud.phone.number"].create(number_data)
                numbers_ids += number_id

        return numbers_ids

    def get_record_mp3_attachment_mango(self, call_id):
        """Запрос mp3 файла записи разговора звонка

        Arguments:
            call_id -- звонок
        """

        path = "/queries/recording/post/"
        json_data = {
            "recording_id": call_id.filename[1:-1],
            "action": "download",
        }
        attachment_raw = self._mango_auth_request(
            self.url + path, json_data=json_data, binary_content=True
        )

        if not attachment_raw:
            return attachment_raw
        attachment = {
            "name": f"{call_id.tel} {call_id.number_id.tel}.mp3",
            "type": "binary",
            "res_id": call_id.id,
            "res_model": call_id._name,
            "datas": base64.b64encode(attachment_raw),
        }
        return attachment

    def create_attachment_mango(self, call_id):
        attachment_mp3 = self.get_record_mp3_attachment_mango(call_id)
        if attachment_mp3:
            attachment_id = self.env["ir.attachment"].create(attachment_mp3)
            call_id.ir_attachment_id = attachment_id

    @staticmethod
    def get_hms(timedelta):
        seconds = timedelta.seconds
        hours = seconds // 3600
        minutes = (seconds // 60) % 60
        return "%02d:%02d:%02d" % (hours, minutes, seconds%60)

    def find_number_by_extension_and_tel_mango(self, call):
        """Определяет подключенный номер из звонка, а также тип звонка.
        Его легко можно найти по extension. Если он не указан
        по самому номеру телефона.

        Arguments:
            call -- звонок (dict)

        Returns:
            number, calltype, calltel
        """
        calltype = "incoming" if call["to_extension"] else "outgoing"
        calltel = call["from_number"] if call["to_extension"] else call["to_number"]
        # ищем по внутреннему номеру но протокол tel
        number = self.env["cloud.phone.number"].search(
            [
                (
                    "extension",
                    "=",
                    call["to_extension"] if call["to_extension"] else call["from_extension"],
                ),
                (
                    "protocol",
                    "=",
                    'tel',
                )
            ],
            limit=1
        )
        # ищем по внутреннему номеру протокол sip
        if not number:
            number = self.env["cloud.phone.number"].search(
            [
                (
                    "extension",
                    "=",
                    call["to_extension"] if call["to_extension"] else call["from_extension"],
                ),
                # (
                #     "protocol",
                #     "=",
                #     'tel',
                # )
            ],
            limit=1
        )
        if not number:
            # если не нашли по extension, пробуем искать по номеру в номерах манго
            # берем только цифры
            phone_to = "".join(i for i in call["to_number"] if i.isdigit())
            phone_from = "".join(i for i in call["from_number"] if i.isdigit())

            calltype = "incoming"
            calltel = call["from_number"]
            number = self.env["cloud.phone.number"].search(
                [
                    (
                        "tel",
                        "=",
                        phone_to,
                    ),
                    (
                        "connector_id",
                        "=",
                        self.id,
                    ),
                ],
                limit=1
            )
            if not number:
                calltype = "outgoing"
                calltel = call["to_number"]
                number = self.env["cloud.phone.number"].search(
                    [
                        (
                            "tel",
                            "=",
                            phone_from,
                        ),
                        (
                            "connector_id",
                            "=",
                            self.id,
                        ),
                    ],
                    limit=1
                )

        return (number,calltype,calltel)

    def get_and_updete_call_mango(self, call):
        """
        Get call from cloud or update if already exist
        update should when run when call already exist
        but not yet have recording
        """
        (number,calltype,calltel) = self.find_number_by_extension_and_tel_mango(call)
        start_datetime = datetime.fromtimestamp(int(call["start"]))
        finish_datetime = datetime.fromtimestamp(int(call["finish"]))
        duration = self.get_hms(finish_datetime - start_datetime)
        call_id = self.env["cloud.phone.call"].search(
            [
                ("time", "=", start_datetime),
                ("call_duration", "=", duration),
                ("number_id.id", "=", number.id),
            ]
        )

        # время самого разговора и время записи
        rec_duration = "00:00:00"
        if int(call["answer"]) > 0:
            start_answer_datetime = datetime.fromtimestamp(int(call["answer"]))
            rec_duration = self.get_hms(finish_datetime - start_answer_datetime)

        # TODO: понять почему line_number from_number и to_number
        # различаются и понять как определить звонок входящий или исходящий
        call_data = dict(
            time=start_datetime,
            number_id=number.id or False,
            type=calltype,
            tel=calltel,
            rec_duration=rec_duration,
            call_duration=duration,
            connector_id=self.id,
            filename=call["records"],
        )

        if not call_id:
            call_id = self.env["cloud.phone.call"].create(call_data)
            # attach mp3 recording of call, if recDuration exist
            if int(call["answer"]) > 0:
                self.create_attachment_mango(call_id)

        # if try get when calling run, can request recording again later
        elif int(call["answer"]) > 0 and not call_id.ir_attachment_id:
            self.create_attachment_mango(call_id)

    def get_and_update_calls_mango(self, begin_datetime, end_datetime):
        # получение ключа для доступа к истории всех звонков за период
        path = "/stats/request"
        json_data = {
            "date_from": begin_datetime,
            "date_to": end_datetime,
        }
        json_data = self._mango_auth_request(self.url + path, json_data=json_data)
        # TODO: work callback
        # because data ready async
        time.sleep(5)
        # получение csv файла истории всех звонков за период
        path = "/stats/result"
        calls = self._mango_auth_request(
            self.url + path, json_data=json_data, binary_content=False, csv_content=True
        )
        for call in calls:
            # если с ответом или исходящий, входящие не сохраняются так как их слишком
            # много из за очереди IVR на каждый вызов примерно 10 входящих
            if int(call["answer"]) > 0 or call["from_extension"]:
                self.get_and_updete_call_mango(call)

    @api.model
    def schedule_connector_mango(
        self, days=None, minutes=60, wait_minutes=60, recreate=False
    ):
        connector_ids = self.search(
            [("active", "=", True), ("cloud_phone_vendor", "=", "mango")]
        )
        for connector in connector_ids:
            # обновление списка подключенных номеров
            connector.get_and_update_numbers_mango()
            connector.get_and_update_numbers_mango2()

            # обновление или добавление звонков и записей звонков, за период
            delta = timedelta(days=days) if days else timedelta(minutes=minutes)
            waiting_time_end_call = timedelta(minutes=wait_minutes)
            connector.get_and_update_calls_mango(
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
                    connector.create_attachment_mango(call_id)
