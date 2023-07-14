import json
import logging

from odoo import http

_logger = logging.getLogger(__name__)


class MangoCall(http.Controller):
    @http.route(
        "/events/call", auth="none", type="http", csrf=False, methods=["POST"]
    )
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
                [("active", "=", True), ("cloud_phone_vendor", "=", "mango")],
                limit=1,
            )
        )

        auth_checked = (
            http.request.env["cloud.phone.connector.factory.mango"]
            .sudo()
            ._auth_check(
                mango_connector,
                kw.get("vpbx_api_key"),
                kw.get("sign"),
                kw.get("json"),
            )
        )
        if not auth_checked:
            return

        call = json.loads(kw.get("json"))

        _logger.info(f"Incoming call: {call}")
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
            ) = (
                http.request.env["cloud.phone.connector.factory.mango"]
                .sudo()
                ._find_number_by_extension_and_tel(mango_connector, call_dict)
            )

            _logger.info(
                f"Incoming call found number: {number.id} {number.tel}"
            )
            # если номер привязан к сотруднику
            if number and number.employee_id and calltype == "incoming":
                # берем только цифры
                phone = "".join(
                    i for i in call["from"]["number"] if i.isdigit()
                )
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
                            ("phone", "=", "8" + phone[1:]),
                            "|",
                            ("mobile", "=", phone),
                            "|",
                            ("mobile", "=", phone[1:]),
                            ("mobile", "=", "8" + phone[1:]),
                        ],
                        limit=1,
                    )
                )
                if partner_id:
                    # отправить на юзера
                    _logger.info(
                        f"Incoming call sendone parnter_id: {number.employee_id.user_id.partner_id.id}"
                    )
                    http.request.env["bus.bus"].sudo().sendone(
                        (
                            http.request._cr.dbname,
                            "res.partner",
                            # partner_id.user_id.id if partner_id.user_id else number.employee_id.user_id.partner_id.id,
                            number.employee_id.user_id.partner_id.id,
                        ),
                        {
                            "type": "mango_call",
                            "title": "Текущий звонок от партнера %s"
                            % partner_id.name,
                            "message": "Вы можете перейти к данному контагенту",
                            "subtype": "Наш партнер",
                            "color": "green",
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
                        _logger.info(
                            f"Incoming call sendone old lead_id: {lead_id}"
                        )
                        http.request.env["bus.bus"].sudo().sendone(
                            (
                                http.request._cr.dbname,
                                "res.partner",
                                lead_id.user_id.partner_id.id
                                if lead_id.user_id
                                else number.employee_id.user_id.partner_id.id,
                            ),
                            {
                                "type": "mango_call",
                                "title": "Текущий звонок от старого лида %s"
                                % phone,
                                "message": "Вы можете перейти к данному старому лиду",
                                "subtype": "Старый лид",
                                "color": "green",
                                "phone": phone,
                                "call": call,
                                "id": lead_id.id,
                                "model": "crm.lead",
                            },
                        )

                    # если это не партнер и не старый лид, значит новый лид
                    else:
                        if number.lead_generation != "no":
                            lead = {
                                "type": "lead",
                                "description": str(call),
                                "name": "Отвеченный звонок",
                                "phone": call["from"]["number"],
                                "mobile": call["from"]["number"],
                                "user_id": number.employee_id.user_id.id
                                if number.lead_generation == "self"
                                else False,
                            }
                            lead_id = (
                                http.request.env["crm.lead"].sudo().create(lead)
                            )
                            _logger.info(
                                f"Incoming call sendone new lead_id: {lead_id}"
                            )
                            http.request.env["bus.bus"].sudo().sendone(
                                (
                                    http.request._cr.dbname,
                                    "res.partner",
                                    number.employee_id.user_id.partner_id.id,
                                ),
                                {
                                    "type": "mango_call",
                                    "title": "Текущий звонок от нового лида %s"
                                    % phone,
                                    "message": "Вы можете перейти к данному  новому лиду",
                                    "subtype": "Новый лид",
                                    "color": "green",
                                    "phone": phone,
                                    "call": call,
                                    "id": lead_id.id,
                                    "model": "crm.lead",
                                },
                            )

        http.request.env["cloud.phone.event"].sudo().create(
            {
                "type": "mango_event_call",
                "connector_id": mango_connector.id,
                "body": "",
                "params": str(kw),
                # "call_from": call["from"]["number"],
                # "call_to": call["to"]["number"],
                # "line_number": call["to"]["line_number"],
                # "disconnect_reason": call["disconnect_reason"],
            }
        )
        return "OK"

    @http.route(
        "/events/summary",
        auth="none",
        type="http",
        csrf=False,
        methods=["POST"],
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

        - call_direction: направление вызова:
            0 – внутренний (между двумя абонентами ВАТС);
            1 – входящий (от внешнего номера абоненту ВАТС);
            2 – исходящий (от абонента ВАТС на внешний номер);

        - from: данные, относящиеся к вызывающему абоненту:
            - extension: внутренний номер (идентификатор) вызывающего абонента (сотрудника
            ВАТС). Подставляется в зависимости от направления вызова:
                - входящий звонок: не передается;
                API MANGO OFFICE | Версия от 17.04.2023
                27
                - исходящий и внутренний звонок: передается, если внутренний номер задан для
            сотрудника, который инициирует вызов;
            - number: номер вызывающего абонента:
                - входящий звонок: номер звонящего (АОН). Если АОН звонящего не определен, не
                передается;
                - исходящий и внутренний звонок: номер, с которого совершает вызов абонент ВАТС;

        - to: данные, относящиеся к вызываемому абоненту. В случае, если в звонок был адресован
            на несколько абонентов в виде цепочки переадресации:
            - при успешном звонке: абонент, который ответил на вызов;
            - при не успешном (пропущенном звонке): первый абонент, который пропустил вызов
            (первое звено цепочки переадресации);
            - extension: внутренний номер (идентификатор) вызываемого абонента или группы. Не
                передается, если у сотрудника ВАТС либо у группы сотрудников ВАТС не задан внутренний
                номер. При исходящих звонках также может определяться, если набранный номер используется
                каким-либо сотрудником в качестве средства приема вызовов;
            - number: номер оконечного устройства вызываемого абонента: номер телефона, номер fmc,
                sip-адрес. Не передается для случая не успешного вызова на группу. При входящем и внутреннем
                звонке в случае одновременного дозвона на несколько устройств, принадлежащих одному
                абоненту ВАТС:
                - при успешном звонке: передается номер устройства, на котором абонент поднял трубку;
                - при не успешном (пропущенном звонке): передается основной номер абонента ВАТС
                (первый в списке номеров в карточке сотрудника);

        - line_number: линия ВАТС, через которую прошел вызов. Подставляется в зависимости от
            направления вызова:
            - если внутренний вызов – не передается;
            - если входящий вызов – линия (номер), на который поступил звонок;
            - если исходящий вызов – линия (номер), через которую звонок вышел из ВАТС;

        entry_result: результат вызова: 1 - звонок успешен и разговор состоялся, 0 - звонок
        пропущен, разговор не состоялся;
        """

        mango_connector = (
            http.request.env["cloud.phone.connector"]
            .sudo()
            .search(
                [("active", "=", True), ("cloud_phone_vendor", "=", "mango")],
                limit=1,
            )
        )

        auth_checked = (
            http.request.env["cloud.phone.connector.factory.mango"]
            .sudo()
            ._auth_check(
                mango_connector,
                kw.get("vpbx_api_key"),
                kw.get("sign"),
                kw.get("json"),
            )
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
            to_extension=call["to"]["extension"]
            if "extension" in call["to"]
            else "",
            to_number=call["to"]["number"],
            disconnect_reason=call["disconnect_reason"],
            line_number=call["line_number"],
            location="abonent",
            call_direction=call["call_direction"],
        )

        (
            number,
            calltype,
            calltel,
        ) = (
            http.request.env["cloud.phone.connector.factory.mango"]
            .sudo()
            ._find_number_by_extension_and_tel(mango_connector, call=call_dict)
        )
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
                        ("phone", "=", "8" + phone[1:]),
                        "|",
                        ("mobile", "=", phone),
                        "|",
                        ("mobile", "=", phone[1:]),
                        ("mobile", "=", "8" + phone[1:]),
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
                        "title": "Пропущенный звонок от партнера %s"
                        % partner_id.name,
                        "message": "Вы можете перейти к данному партнеру",
                        "subtype": "Пропущенный от партнера",
                        "color": "red",
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
                user_id = (
                    number.employee_id.user_id.id
                    if number.lead_generation == "self"
                    else False
                )
                # если звонок поступил на линию, отличную от той на которой был начат звонок
                # т.е. например IVR то тогда при пропущенном, в лиде менеджер будет установлен
                # первый из очереди. но нам нужно сделать общего лида без привязки к менеджеру
                if number.tel != call["line_number"]:
                    user_id = False
                lead = {
                    "type": "lead",
                    "user_id": user_id,
                    "description": str(call),
                    "name": "Пропущенный звонок",
                    "phone": call["from"]["number"],
                    "mobile": call["from"]["number"],
                }
                if number.lead_generation != "no":
                    lead_id = http.request.env["crm.lead"].sudo().create(lead)
            if number.employee_id and number.lead_generation != "no":
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
                        "color": "red",
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
                http.request.env[
                    "cloud.phone.connector.factory.mango"
                ].sudo()._get_and_update_call(mango_connector, call_dict)

        # в любом случае создать событие в системе
        http.request.env["cloud.phone.event"].sudo().create(
            {
                "type": "mango_event_summary",
                "connector_id": mango_connector.id,
                "body": "",
                "params": str(kw),
                "call_from": call["from"]["number"],
                "call_to": call["to"]["number"],
                "line_number": call["line_number"],
                "disconnect_reason": call["disconnect_reason"],
            }
        )
        return "OK"
