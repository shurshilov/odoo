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
        body = http.request.httprequest.data
        mango_connector = (
            http.request.env["cloud.phone.connector"]
            .sudo()
            .search([("cloud_phone_vendor", "=", "mango")], limit=1)
        )

        auth_checked = mango_connector._mango_auth_check(
            kw.get("vpbx_api_key"), kw.get("sign"), kw.get("json")
        )
        if not auth_checked:
            return

        call = json.loads(kw.get("json"))

        # если вызов на который ответили (сняли трубку)
        if (
            call["call_state"] == "Connected"
            and call["location"] == "abonent"
            and "extension" in call["to"]
        ):
            number = (
                http.request.env["cloud.phone.number"]
                .sudo()
                .search(
                    [
                        (
                            "extension",
                            "=",
                            call["to"]["extension"],
                        ),
                        (
                            "protocol",
                            "=",
                            "tel",
                        ),
                    ],
                    limit=1,
                )
            )
            # берем только цифры
            phone = "".join(i for i in call["from"]["number"] if i.isdigit())

            if number:
                # ищем партнера
                partner_id = (
                    http.request.env["res.partner"]
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
                if partner_id:
                    # отправить на клиента форму партнера
                    http.request.env["bus.bus"].sudo().sendone(
                        (
                            http.request._cr.dbname,
                            "res.partner",
                            number.employee_id.user_id.partner_id.id,
                        ),
                        {
                            "type": "mango_call",
                            "title": "Звонок от партнера %s" % partner_id.name,
                            "message": "Вы можете перейти к данному контагенту",
                            "subtype": "Наш партнер",
                            "name": partner_id.name,
                            "phone": phone,
                            "call": call,
                            "id": partner_id.id,
                            "model": "res.partner",
                            "user_id": number.employee_id.user_id.id,
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
                        # отправить на клиента форму лида
                        http.request.env["bus.bus"].sudo().sendone(
                            (
                                http.request._cr.dbname,
                                "res.partner",
                                number.employee_id.user_id.partner_id.id,
                            ),
                            # (http.request._cr.dbname, "res.partner", 3),
                            {
                                "type": "mango_call",
                                "title": "Звонок от старого лида %s" % phone,
                                "message": "Вы можете перейти к данному старому лиду",
                                "subtype": "Старый лид",
                                "phone": phone,
                                "call": call,
                                "id": lead_id.id,
                                "model": "crm.lead",
                                "user_id": number.employee_id.user_id.id,
                            },
                        )

                    # если это не партнер и не старый лид, значит новый лид
                    else:
                        lead = {
                            "type": "lead",
                            "user_id": False,
                            "description": str(call["to"])
                            + "\n"
                            + str(call["taken_from_call_id"]),
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
                                "title": "Звонок от нового лида %s" % phone,
                                "message": "Вы можете перейти к данному  новому лиду",
                                "subtype": "Новый лид",
                                "phone": phone,
                                "call": call,
                                "id": lead_id.id,
                                "model": "crm.lead",
                                "user_id": number.employee_id.user_id.id,
                            },
                        )

        http.request.env["cloud.phone.event"].sudo().create(
            {
                "type": "mango_event_call",
                "body": body.decode("utf-8"),
                "params": str(kw),
                "call_from": call["from"]["number"],
                "call_to": call["to"]["number"],
                "line_number": call["to"]["line_number"],
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

        body = http.request.httprequest.data
        mango_connector = (
            http.request.env["cloud.phone.connector"]
            .sudo()
            .search([("cloud_phone_vendor", "=", "mango")], limit=1)
        )

        auth_checked = mango_connector._mango_auth_check(
            kw.get("vpbx_api_key"), kw.get("sign"), kw.get("json")
        )
        if not auth_checked:
            return

        call = json.loads(kw.get("json"))

        # если звонок пропущен всеми менеджерами, и это не партнер, создать лид
        if not call["entry_result"]:
            # берем только цифры
            phone = "".join(i for i in call["from"]["number"] if i.isdigit())

            # ищем партнера
            partner_id = (
                http.request.env["res.partner"]
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

            # если это не партнер, значит лид, удаляем сип номера (внутренние)
            if not partner_id and "sip" not in call["from"]["number"]:
                lead = {
                    "type": "lead",
                    "user_id": False,
                    "description": str(call["to"])
                    + "\n"
                    + call["line_number"]
                    + "\n"
                    + str(call["disconnect_reason"])
                    + "\n"
                    + str(call["create_time"]),
                    "name": "Пропущенный звонок",
                    "phone": call["from"]["number"],
                    "mobile": call["from"]["number"],
                }
                lead_id = http.request.env["crm.lead"].sudo().create(lead)
        # в любом случае создать событие в системе
        http.request.env["cloud.phone.event"].sudo().create(
            {
                "type": "mango_event_summary",
                "body": body.decode("utf-8"),
                "params": str(kw),
                "call_from": call["from"]["number"],
                "call_to": call["to"]["number"],
                "line_number": call["line_number"],
                "disconnect_reason": call["disconnect_reason"],
            }
        )
