# -*- coding: utf-8 -*-
from odoo import http
import json


class MangoCall(http.Controller):
    @http.route("/events/call", auth="none", type="http", csrf=False, methods=["POST"])
    def events_call(self, **kw):
        """Уведомление содержит информацию о вызове и его параметрах. Прохождение вызова через
        IVR, очередь вызовов, размещение на абонента сопровождаются рассылкой уведомления о новом
        вызове. Завершение пребывания в очереди IVR сопровождается рассылкой события о
        завершении соответствующего вызова
        Пример вызова:
        {
            "entry_id":"MTYxNzM5NjY0OTE=","call_id":"MToxMDA4NjI3Nzo1MDI6NjQ0MjQzNTM5",
            "timestamp":1670060542,"seq":2,
            "call_state":"Connected",
            "location":"abonent",
            "from":{"number":"79607164646",
            "taken_from_call_id":"MToxMDA4NjI3Nzo1MDI6NjQ0MjQzNTMyOjE="},
            "to":{"extension":"222","number":"79776307393","line_number":"sip:roistat-0758@vpbx400076322.mangosip.ru","acd_group":"999"},
            "dct":{"type":0}
        }
        """
        mango_connector = (
            http.request.env["cloud.phone.connector"]
            .sudo()
            .search(
                [("active", "=", True), ("cloud_phone_vendor", "=", "mango")], limit=1
            )
        )

        auth_checked = mango_connector._mango_auth_check(
            kw.get("vpbx_api_key"), kw.get("sign"), kw.get("json")
        )
        if not auth_checked:
            return

        call = json.loads(kw.get("json"))

        # если вызов на который ответили (сняли трубку) и вызов сотруднику и не с внутреннего номера
        # значит разговариваем с клиентом
        if (
            call["call_state"] == "Connected"
            and call["location"] == "abonent"
            and "extension" in call["to"]
            and "extension" not in call["from"]
            and "sip" not in call["from"]["number"]
        ):
            # парсим событие в массив звонка
            call_dict = dict(
                from_extension=call["from"]["extension"]
                if "extension" in call["from"]
                else "",
                from_number=call["from"]["number"],
                to_extension=call["to"]["extension"]
                if "extension" in call["to"]
                else "",
                to_number=call["to"]["number"],
            )
            (
                number,
                calltype,
                calltel,
            ) = mango_connector.find_number_by_extension_and_tel_mango(call_dict)

            # если номер привязан к сотруднику
            if number and number.employee_id and calltype == "incoming":
                # берем только цифры
                phone = "".join(i for i in call["from"]["number"] if i.isdigit())
                # ищем партнера
                partner_id = (
                    http.request.env["res.partner"]
                    .sudo()
                    .search(
                        [
                            "|",
                            ("phone", "=", phone),
                            "|",
                            ("phone", "=", phone[1:]),
                            "|",
                            ("phone", "=", "8"+phone[1:]),
                            "|",
                            ("mobile", "=", phone),
                            "|",
                            ("mobile", "=", phone[1:]),
                            ("mobile", "=", "8"+phone[1:]),
                        ],
                        limit=1,
                    )
                )
                if partner_id:
                    # отправить на юзера
                    http.request.env["bus.bus"].sudo().sendone(
                        (
                            http.request._cr.dbname,
                            "res.partner",
                            number.employee_id.user_id.partner_id.id,
                        ),
                        {
                            "type": "mango_call",
                            "title": "Текущий звонок от партнера %s" % partner_id.name,
                            "message": "Вы можете перейти к данному контагенту",
                            "subtype": "Наш партнер",
                            "color":"green",
                            "name": partner_id.name,
                            "phone": phone,
                            "call": call,
                            "id": partner_id.id,
                            "model": "res.partner",
                        },
                    )

                else:
                    # ищем лида
                    lead_id = (
                        http.request.env["crm.lead"]
                        .sudo()
                        .search(
                            [
                                "|",
                                ("phone", "=", phone[1:]),
                                "|",
                                ("phone", "=", phone),
                                "|",
                                ("mobile", "=", phone),
                                ("mobile", "=", phone[1:]),
                            ],
                            limit=1,
                        )
                    )
                    if lead_id:
                        # поднимаем лида вверх
                        priority_old = int(lead_id.priority)
                        if priority_old < 3:
                            priority_old += 1
                            lead_id.priority = str(priority_old)
                        # отправить на юзера
                        http.request.env["bus.bus"].sudo().sendone(
                            (
                                http.request._cr.dbname,
                                "res.partner",
                                number.employee_id.user_id.partner_id.id,
                            ),
                            {
                                "type": "mango_call",
                                "title": "Текущий звонок от старого лида %s" % phone,
                                "message": "Вы можете перейти к данному старому лиду",
                                "subtype": "Старый лид",
                                "color":"green",
                                "phone": phone,
                                "call": call,
                                "id": lead_id.id,
                                "model": "crm.lead",
                            },
                        )

                    # если это не партнер и не старый лид, значит новый лид
                    else:
                        lead = {
                            "type": "lead",
                            "description": str(call),
                            "name": "Отвеченный звонок",
                            "phone": call["from"]["number"],
                            "mobile": call["from"]["number"],
                            "user_id": number.employee_id.user_id.id,
                        }
                        lead_id = http.request.env["crm.lead"].sudo().create(lead)
                        http.request.env["bus.bus"].sudo().sendone(
                            (
                                http.request._cr.dbname,
                                "res.partner",
                                number.employee_id.user_id.partner_id.id,
                            ),
                            {
                                "type": "mango_call",
                                "title": "Текущий звонок от нового лида %s" % phone,
                                "message": "Вы можете перейти к данному  новому лиду",
                                "subtype": "Новый лид",
                                "color":"green",
                                "phone": phone,
                                "call": call,
                                "id": lead_id.id,
                                "model": "crm.lead",
                            },
                        )

        http.request.env["cloud.phone.event"].sudo().create(
            {
                "type": "mango_event_call",
                "body": "",
                "params": str(kw),
                #"call_from": call["from"]["number"],
                #"call_to": call["to"]["number"],
                # "line_number": call["to"]["line_number"],
                # "disconnect_reason": call["disconnect_reason"],
            }
        )

    @http.route(
        "/events/summary", auth="none", type="http", csrf=False, methods=["POST"]
    )
    def events_summary(self, **kw):
        """Уведомление содержит основную информацию о звонке после его окончания и служит
        индикатором окончания разговора.
        Генерируется как финализирующее событие по звонку. После получения данного события
        вызов можно считать завершенным
        Пример:
        {
        "entry_id":"MTYxNzM5NjY0OTE=","call_direction":1,
        "from":{"number":"79607164646"},
        "to":{"extension":"222","number":"79776307393"},
        "line_number":"sip:roistat-0758@vpbx400076322.mangosip.ru",
        "create_time":1670060527,"forward_time":1670060527,"talk_time":1670060542,"end_time":1670060661,
        "entry_result":1,
        "disconnect_reason":1110
        }

        entry_result: результат вызова: 1 - звонок успешен и разговор состоялся, 0 - звонок
        пропущен, разговор не состоялся;
        """

        mango_connector = (
            http.request.env["cloud.phone.connector"]
            .sudo()
            .search(
                [("active", "=", True), ("cloud_phone_vendor", "=", "mango")], limit=1
            )
        )

        auth_checked = mango_connector._mango_auth_check(
            kw.get("vpbx_api_key"), kw.get("sign"), kw.get("json")
        )
        if not auth_checked:
            return

        call = json.loads(kw.get("json"))

        # парсим событие в массив звонка
        call_dict = dict(
            records="пропущенный, записи нет",
            start=call["create_time"],
            finish=call["end_time"],
            answer="0",
            from_extension=call["from"]["extension"]
            if "extension" in call["from"]
            else "",
            from_number=call["from"]["number"],
            to_extension=call["to"]["extension"] if "extension" in call["to"] else "",
            to_number=call["to"]["number"],
            disconnect_reason=call["disconnect_reason"],
            line_number=call["line_number"],
            location="abonent",
        )

        (
            number,
            calltype,
            calltel,
        ) = mango_connector.find_number_by_extension_and_tel_mango(call=call_dict)
        # если звонок не состоялся и он входящий и не с внутреннего номера
        # значит он пропущенный входящий от клиента
        if (
            number
            and not call["entry_result"]
            and calltype == "incoming"
            and "extension" not in call["from"]
            and "sip" not in call["from"]["number"]
        ):
            # берем только цифры
            phone = "".join(i for i in call["from"]["number"] if i.isdigit())

            # ищем партнера
            partner_id = (
                http.request.env["res.partner"]
                .sudo()
                .search(
                    [
                        "|",
                        ("phone", "=", phone),
                        "|",
                        ("phone", "=", phone[1:]),
                        "|",
                        ("phone", "=", "8"+phone[1:]),
                        "|",
                        ("mobile", "=", phone),
                        "|",
                        ("mobile", "=", phone[1:]),
                        ("mobile", "=", "8"+phone[1:]),
                    ],
                    limit=1,
                )
            )
            if partner_id and number.employee_id:
                # отправить на юзера
                http.request.env["bus.bus"].sudo().sendone(
                    (
                        http.request._cr.dbname,
                        "res.partner",
                        number.employee_id.user_id.partner_id.id,
                    ),
                    {
                        "type": "mango_call",
                        "title": "Пропущенный звонок от партнера %s" % partner_id.name,
                        "message": "Вы можете перейти к данному партнеру",
                        "subtype": "Пропущенный от партнера",
                        "color":"red",
                        "phone": phone,
                        "call": call,
                        "id": partner_id.id,
                        "model": "res.partner",
                    },
                )
            # ищем лида
            lead_id = (
                http.request.env["crm.lead"]
                .sudo()
                .search(
                    [
                        "|",
                        ("phone", "=", phone[1:]),
                        "|",
                        ("phone", "=", phone),
                        "|",
                        ("mobile", "=", phone),
                        ("mobile", "=", phone[1:]),
                    ],
                    limit=1,
                )
            )
            if lead_id:
                # поднимаем лида вверх
                priority_old = int(lead_id.priority)
                if priority_old < 3:
                    priority_old += 1
                    lead_id.priority = str(priority_old)

            # если это не партнер и не старый лид, то новый лид
            new = False
            if not partner_id and not lead_id:
                new = True
                lead = {
                    "type": "lead",
                    "user_id": number.employee_id.user_id.id
                    if number.employee_id
                    else False,
                    "description": str(call),
                    "name": "Пропущенный звонок",
                    "phone": call["from"]["number"],
                    "mobile": call["from"]["number"],
                }
                lead_id = http.request.env["crm.lead"].sudo().create(lead)
            if number.employee_id:
                # отправить на юзера
                http.request.env["bus.bus"].sudo().sendone(
                    (
                        http.request._cr.dbname,
                        "res.partner",
                        number.employee_id.user_id.partner_id.id,
                    ),
                    {
                        "type": "mango_call",
                        "title": "Пропущенный звонок от нового лида %s" % phone
                        if new
                        else "Пропущенный звонок от старого лида %s" % phone,
                        "message": "Вы можете перейти к данному новому лиду"
                        if new
                        else "Вы можете перейти к данному старому лиду",
                        "subtype": "Пропущенный от старого лида",
                        "color":"red",
                        "phone": phone,
                        "call": call,
                        "id": lead_id.id,
                        "model": "crm.lead",
                    },
                )
            # создать пропущенный входящий звонок в истории звонков
            # так как изначально в истории только звонки с записью или исходящие без записи(когда звонок не состоялся)
            # то здесь мы сохраняем входящие без записи. Сразу это не делается так как
            # входящих из-за IVR очереди слишком много и они будут мешать, к примеру на 1 лид:
            # будет создано 10 звонков из который 2 IVR 7 входящих не отвеч на менеджеров и 1 отвеченный
            # итого 10. Если никто не ответил, то 2 IVR 8 входящих не отвеч на менеджеров
            # итого 10 звонков в истории тоже.
            # Это больше внутренняя информаци и для менеджеров не нужна. В текущей реализации будет 1
            # неотвеченный или 1 отвеченный.
            # А в общей истории звонков events будут все звонки 10(штук) + 1 завершающее событие.

            # добавить пропущенный звонок в историю звонков
            # пропущенные могут быть с записью и тогда их не создаем, т.к. они уже есть
            if call["talk_time"] == 0:
                mango_connector.get_and_updete_call_mango(call_dict)

        # в любом случае создать событие в системе
        http.request.env["cloud.phone.event"].sudo().create(
            {
                "type": "mango_event_summary",
                "body": "",
                "params": str(kw),
                "call_from": call["from"]["number"],
                "call_to": call["to"]["number"],
                "line_number": call["line_number"],
                "disconnect_reason": call["disconnect_reason"],
            }
        )
