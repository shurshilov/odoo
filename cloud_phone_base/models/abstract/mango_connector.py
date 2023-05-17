# -*- coding: utf-8 -*-

import base64
import json
import requests
import time
from hashlib import sha256
from datetime import datetime
from requests.exceptions import Timeout

from odoo import models
from odoo.exceptions import ValidationError


class CloudPhoneConnectorMango(models.AbstractModel):
    """Mango connector

    Arguments:
        url --  https://app.mango-office.ru/vpbx
    """

    _name = "cloud.phone.connector.factory.mango"
    _inherit = "cloud.phone.connector.factory"

    def _auth_check(self, connector_id, vpbx_api_key, sign, json_str):
        """Проверяет подпись и апи ключ во входящем запросе

        Arguments:
            vpbx_api_key -- апи ключ
            sign -- подпись
            json -- полезные данные

        Returns:
            проверка пройдена или нет
        """

        if connector_id.vpbx_api_key != vpbx_api_key:
            return False

        # генерируем подпись
        sign_old = sha256(
            (vpbx_api_key + json_str + connector_id.vpbx_api_salt).encode("utf-8")
        ).hexdigest()
        if sign != sign_old:
            False

        return True

    def _auth_request(
        self, connector_id, path, json_data={}, binary_content=False, csv_content=False
    ):
        try:
            # генерируем подпись
            sign = sha256(
                (
                    connector_id.vpbx_api_key
                    + json.dumps(json_data)
                    + connector_id.vpbx_api_salt
                ).encode("utf-8")
            ).hexdigest()
            data = {
                "vpbx_api_key": connector_id.vpbx_api_key,
                "sign": sign,
                "json": json.dumps(json_data),
            }

            response = requests.post(connector_id.url + path, data=data)
            if response.status_code == 404:
                return {}
            if binary_content:
                return response.content
            else:
                if csv_content:
                    import io

                    try:
                        import csv
                    except ImportError:
                        raise ValidationError("Cannot import csv lib!")
                    # обработка строки csv файла
                    try:
                        data_file = io.StringIO(response.text)
                        data_file.seek(0)
                        file_reader = []
                        csv_reader = csv.reader(data_file, delimiter=";")
                        file_reader.extend(csv_reader)
                    except Exception as e:
                        raise ValidationError("Invalid file!")
                    keys = [
                        "records",
                        "start",
                        "finish",
                        "answer",
                        "from_extension",
                        "from_number",
                        "to_extension",
                        "to_number",
                        "disconnect_reason",
                        "line_number",
                        "location",
                        "create",
                        "entry_id",
                    ]
                    values = []
                    for i in range(len(file_reader)):
                        field = list(map(str, file_reader[i]))
                        count = 1
                        count_keys = len(keys)
                        if len(field) > count_keys:
                            for new_fields in field:
                                if count > count_keys:
                                    keys.append(new_fields)
                                count += 1
                        values.append(dict(zip(keys, field)))
                    return values
                return json.loads(response.text) if response.text else []
        except Timeout as e:
            raise ValidationError("Request timeout error " + str(e))
        except Exception as e:
            raise ValidationError("Request unknown error " + str(e))

    def _get_and_update_numbers(self, connector_id):
        """
        Create or update numbers
        Return set or numbers
        """
        path = "/config/users/request"
        numbers = self._auth_request(connector_id, path)
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
                    connector_id=connector_id.id,
                    protocol=number["protocol"],
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

        numbers_ids2 = self._get_and_update_numbers2(connector_id)
        return numbers_ids + numbers_ids2

    def _get_and_update_numbers2(self, connector_id):
        """
        Create or update numbers
        Return set or numbers
        """
        path = "/incominglines"
        numbers = self._auth_request(connector_id, path)
        numbers_ids = self.env["cloud.phone.number"]
        for number in numbers["lines"]:
            employee_id = self.find_by_number("hr.employee", number["number"])

            number_data = dict(
                tel=number["number"],
                employee_id=employee_id.id if employee_id else False,
                comment=number["comment"],
                schema_name=number["schema_name"],
                name=number["name"],
                connector_id=connector_id.id,
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

    def _get_record_mp3_attachment(self, connector_id, call_id):
        """Запрос mp3 файла записи разговора звонка

        Arguments:
            call_id -- звонок
        """

        path = "/queries/recording/post/"
        json_data = {
            "recording_id": call_id.filename[1:-1],
            "action": "download",
        }
        attachment_raw = self._auth_request(
            connector_id, path, json_data=json_data, binary_content=True
        )

        if not attachment_raw:
            return attachment_raw
        attachment = {
            "name": f"{call_id.type} {''.join(i for i in call_id.number_id.tel if i.isdigit())} {call_id.tel}.mp3",
            "type": "binary",
            "res_id": call_id.id,
            "res_model": call_id._name,
            "datas": base64.b64encode(attachment_raw),
        }
        return attachment

    def _create_attachment(self, connector_id, call_id):
        attachment_mp3 = self._get_record_mp3_attachment(connector_id, call_id)
        if attachment_mp3:
            attachment_id = self.env["ir.attachment"].create(attachment_mp3)
            call_id.ir_attachment_id = attachment_id

    def _find_number_by_extension_and_tel(self, connector_id, call):
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
        # поле call_direction есть только в событии результата звонка
        # но его нет в самом звонке
        # calltype = "incoming" if call["call_direction"] == 0 or 1 else "outgoing"
        # calltel = call["from_number"] if calltype == "incoming" else call["to_number"]
        # ищем по внутреннему номеру но протокол tel
        number = self.env["cloud.phone.number"].search(
            [
                (
                    "extension",
                    "=",
                    call["to_extension"]
                    if call["to_extension"]
                    else call["from_extension"],
                ),
                (
                    "protocol",
                    "=",
                    "tel",
                ),
            ],
            limit=1,
        )
        # ищем по внутреннему номеру протокол sip
        if not number:
            number = self.env["cloud.phone.number"].search(
                [
                    (
                        "extension",
                        "=",
                        call["to_extension"]
                        if call["to_extension"]
                        else call["from_extension"],
                    ),
                    # (
                    #     "protocol",
                    #     "=",
                    #     'tel',
                    # )
                ],
                limit=1,
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
                        connector_id.id,
                    ),
                ],
                limit=1,
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
                            connector_id.id,
                        ),
                    ],
                    limit=1,
                )

        return (number, calltype, calltel)

    def _get_and_update_call(self, connector_id, call):
        """
        Get call from cloud or update if already exist
        update should when run when call already exist
        but not yet have recording
        """
        (number, calltype, calltel) = self._find_number_by_extension_and_tel(connector_id, call)
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
            connector_id=connector_id.id,
            filename=call["records"],
        )

        if not call_id:
            call_id = self.env["cloud.phone.call"].create(call_data)
            # attach mp3 recording of call, if recDuration exist
            if int(call["answer"]) > 0:
                self._create_attachment(connector_id, call_id)

        # if try get when calling run, can request recording again later
        elif int(call["answer"]) > 0 and not call_id.ir_attachment_id:
            self._create_attachment(connector_id, call_id)

    def _get_and_update_calls(self, connector_id, begin_datetime, end_datetime):
        # получение ключа для доступа к истории всех звонков за период
        path = "/stats/request"
        json_data = {
            "date_from": begin_datetime,
            "date_to": end_datetime,
        }
        json_data = self._auth_request(connector_id, path, json_data=json_data)
        # TODO: work callback
        # because data ready async
        time.sleep(5)
        # получение csv файла истории всех звонков за период
        path = "/stats/result"
        calls = self._auth_request(
            connector_id, path,
            json_data=json_data,
            binary_content=False,
            csv_content=True,
        )
        for call in calls:
            # если с ответом или исходящий, входящие не сохраняются так как их слишком
            # много из за очереди IVR на каждый вызов примерно 10 входящих
            if int(call["answer"]) > 0 or call["from_extension"]:
                self._get_and_update_call(connector_id, call)
