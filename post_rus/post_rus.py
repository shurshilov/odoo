# Copyright 2018 Artem Shurshilov
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
import io
import zipfile

# import cStringIO
try:
    from StringIO import StringIO  # # for Python 2
except ImportError:
    from io import StringIO  ## for Python 3

import base64
import csv
import json
import math
import urllib

import requests
from odoo import api, exceptions, fields, models
from PyPDF2 import PdfFileMerger, PdfFileReader
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas


class res_company(models.Model):
    _name = "res.company"
    _inherit = ["res.company"]

    accessToken = fields.Char(string="Application Authentication Token")
    protocol = fields.Char(string="Protocol connection", default="https://")
    host = fields.Char(
        string="Address api request", default="otpravka-api.pochta.ru"
    )


class res_users(models.Model):
    _name = "res.users"
    _inherit = ["res.users"]

    basicToken = fields.Char(string="User Authentication Key")


class delivery_carrier(models.Model):
    _name = "delivery.carrier"
    _inherit = ["delivery.carrier"]

    name_del = fields.Char(string="Name of delivery")


class sale_order(models.Model):
    _name = "sale.order"
    _inherit = ["sale.order"]

    @api.onchange("payment_term_id")
    def dymamic_domen(self):
        if self.payment_term_id.name == "Предоплата (100%)":
            return {
                "domain": {
                    "carrier_id": [
                        ("name_del", "in", ["ПР 1-й класс", "ПР", "EMS"])
                    ]
                }
            }
        if self.payment_term_id.name == "Наложенный платеж ПР":
            return {
                "domain": {
                    "carrier_id": [
                        (
                            "name_del",
                            "in",
                            [
                                "ПР 1-й класс наложка",
                                "ПР наложка",
                                "EMS наложка",
                            ],
                        )
                    ]
                }
            }
        return {"domain": {"carrier_id": [("id", ">", 0)]}}


class stock_picking(models.Model):
    _name = "stock.picking"
    _inherit = ["stock.picking"]

    # may be one2many in future
    post_order_id = fields.Many2one(
        string="Post order", comodel_name="post.order"
    )
    post_count = fields.Integer(
        string="Post Orders", compute="_compute_post_ids"
    )

    # @api.multi
    def merge_all_pdf(self):
        """
        Merge all post rus attachment and download it
        """
        merger = PdfFileMerger()
        for rec in self:
            attach_ids = self.env["ir.attachment"].search(
                [
                    (
                        "name",
                        "=",
                        "Скачать файл для печати "
                        + str(rec.post_order_id.id_post).decode("utf-8"),
                    ),
                    ("type", "=", "binary"),
                    ("res_id", "=", rec.id),
                    ("res_model", "=", "stock.picking"),
                ],
                limit=1,
            )
            for attach_id in attach_ids:
                if self.env["stock.picking"].browse(rec.id).state == "assigned":
                    input_rec = PdfFileReader(
                        io.BytesIO(base64.b64decode(attach_id.datas))
                    )
                    merger.append(input_rec)

        myio = StringIO()
        merger.write(myio)
        datas = myio.getvalue()
        merger.close()
        myio.close()

        [
            attach_id.unlink()
            for attach_id in self.env["ir.attachment"].search(
                [("name", "=", "TEMP POST RUS")]
            )
        ]
        attachment = {
            "name": "TEMP POST RUS",
            "type": "binary",
            "user_id": self.env.user.id,
            "res_model": self._name,
            "datas": base64.b64encode(datas),
            "datas_fname": "all delivery order.pdf",
        }
        temp = self.env["ir.attachment"].create(attachment)
        return {
            "type": "ir.actions.act_url",
            #'url': "/web/content/"+str(temp.id)+"?download=true",
            "url": "/web/content/" + str(temp.id),
            "target": "new",
        }

    # @api.multi
    @api.depends("post_order_id")
    def _compute_post_ids(self):
        for rec in self:
            order_ids = self.env["post.order"].search(
                [("delivery_order_id.id", "=", rec.id)]
            )
            rec.post_count = len(order_ids)

    # @api.multi
    def action_view_post(self):
        """
        Furure to use One2many post_order_id
        """
        view_id = self.env["ir.model.data"].get_object_reference(
            "post_rus", "post_form_view"
        )[1]
        action = {
            "type": "ir.actions.act_window",
            "view_type": "form",
            "view_mode": "form",
            "view_id": view_id,
            "res_model": "post.order",
            "res_id": self.post_order_id.id,
        }
        # pickings = [self.post_order_id.id]
        # if len(pickings) > 1:
        #     action['domain'] = [('id', 'in', pickings)]
        # elif pickings:
        #     action['views'] = [(self.env.ref('post_rus.post_form_view').id, 'form')]
        #     action['res_id'] = pickings[0]
        # raise exceptions.ValidationError(str(action))
        return action

    # @api.multi
    def write(self, vals):
        res = super().write(vals)
        if self.state == "assigned" and self.carrier_id.name in [
            "ПР 1-й класс",
            "ПР",
            "EMS",
            "ПР 1-й класс наложка",
            "ПР наложка",
            "EMS наложка",
        ]:
            # mass = sum product weight
            total_weight = sum(
                [
                    line.product_id.weight
                    for line in self.pack_operation_product_ids
                ]
            )
            # сумма обьявленной ценности = sum product standart_price
            # raise exceptions.ValidationError(line.product_id.lst_price )
            total_price = sum(
                [
                    line.product_id.lst_price
                    for line in self.pack_operation_product_ids
                ]
            )
            percent = 0
            fix = 0
            for i in self.sale_id.payment_term_id.line_ids:
                if i.value == "percent":
                    percent += i.value_amount
                if i.value == "fixed":
                    fix += i.value_amount
                # ('balance', 'Balance'),
            po_id = ""
            map_delivery = {
                "ПР 1-й класс": ["PARCEL_CLASS_1", "WITH_DECLARED_VALUE"],
                "ПР": ["ONLINE_PARCEL", "WITH_DECLARED_VALUE"],
                "EMS": ["EMS", "WITH_DECLARED_VALUE"],
                "ПР 1-й класс наложка": [
                    "PARCEL_CLASS_1",
                    "WITH_DECLARED_VALUE_AND_CASH_ON_DELIVERY",
                ],
                "ПР наложка": [
                    "ONLINE_PARCEL",
                    "WITH_DECLARED_VALUE_AND_CASH_ON_DELIVERY",
                ],
                "EMS наложка": [
                    "EMS",
                    "WITH_DECLARED_VALUE_AND_CASH_ON_DELIVERY",
                ],
            }
            md = map_delivery.get(self.sale_id.carrier_id.name_del, False)
            # raise exceptions.ValidationError(self.sale_id.carrier_id.name_del)
            # raise exceptions.ValidationError(md)
            mail_type = md[0] if md else "PARCEL_CLASS_1"
            mail_category = (
                md[1] if md else "WITH_DECLARED_VALUE_AND_CASH_ON_DELIVERY"
            )

            if self.post_order_id:
                # raise exceptions.ValidationError(self.post_order_id)
                po_id = self.env["post.order"].browse(self.post_order_id.id)
                po_id.write(
                    {
                        "state": "new",
                        "recipient_name": self.partner_id.name,
                        "sale_order_id": self.sale_id.id,
                        "tel_address": self.partner_id.phone,
                        "mass": str(int(total_weight * 1000)),
                        "insr_value": math.ceil(total_price / 100) * 100,
                        # наложенный платеж = сумма заказа - аванс(как в процентах так и фиксированный)
                        "payment": int(
                            total_price
                            - ((total_price * percent) / 100.0)
                            - fix
                        ),
                        "address": self.partner_id._display_address(True),
                        "mail_type": mail_type,
                        "mail_category": mail_category,
                        "delivery_order_id": self.id,
                    }
                )
                po_id.document_to_attachment(
                    po_id.id_package, po_id.id_post, "stock.picking"
                )
                po_id.merger_pdf()
            else:
                # Create post.order
                po_id = self.env["post.order"].create(
                    {
                        "state": "new",
                        "recipient_name": self.partner_id.name,
                        "sale_order_id": self.sale_id.id,
                        "tel_address": self.partner_id.phone,
                        "mass": str(
                            int(total_weight * 1000)
                            if int(total_weight * 1000) > 0
                            else 1
                        ),
                        "insr_value": math.ceil(total_price / 100) * 100,
                        # наложенный платеж = сумма заказа - аванс(как в процентах так и фиксированный)
                        "payment": int(
                            total_price
                            - ((total_price * percent) / 100.0)
                            - fix
                        ),
                        "address": self.partner_id._display_address(True),
                        "mail_type": mail_type,
                        "mail_category": mail_category,
                        "delivery_order_id": self.id,
                    }
                )
                # raise exceptions.ValidationError(mass)
                vals["post_order_id"] = po_id.id
                po_id.to_surrender()
                po_id.document_to_attachment(
                    po_id.id_package, po_id.id_post, self.id, "stock.picking"
                )
                po_id.merger_pdf()
                res = super().write(vals)
            attach_ids = self.env["ir.attachment"].search(
                [
                    (
                        "name",
                        "=",
                        "Скачать файл для печати "
                        + str(po_id.id_post).decode("utf-8"),
                    ),
                    ("type", "=", "binary"),
                    ("res_id", "=", po_id.id),
                    ("res_model", "=", "post.order"),
                ],
                limit=1,
            )
            for attach_id in attach_ids:
                # raise exceptions.ValidationError(attach_id.id)
                attach_obj = self.env["ir.attachment"].browse(attach_id.id)
                attachment = {
                    "name": attach_obj.name,
                    "type": attach_obj.type,
                    "user_id": self.env.user.id,
                    "res_id": self.id,
                    "res_model": self._name,
                    "datas": attach_obj.datas,
                    "datas_fname": attach_obj.datas_fname,
                }
                self.env["ir.attachment"].create(attachment)

        return res


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    @api.model
    def _get_company(self):
        return self.env.user.company_id

    default_mail_type = fields.Selection(
        selection=[
            ("POSTAL_PARCEL", 'Посылка "нестандартная"'),
            ("ONLINE_PARCEL", 'Посылка "онлайн"'),
            ("ONLINE_COURIER", 'Курьер "онлайн"'),
            ("EMS", "Отправление EMS"),
            ("EMS_OPTIMAL", "EMS оптимальное"),
            ("LETTER", "Письмо"),
            ("BANDEROL", "Бандероль"),
            ("BUSINESS_COURIER", "Бизнес курьер"),
            ("BUSINESS_COURIER_ES", "Бизнес курьер экпресс"),
            ("PARCEL_CLASS_1", "Посылка 1-го класса"),
        ],
        string="Тип отправления (Вид РПО)",
        default="PARCEL_CLASS_1",
        default_model="post.order",
    )

    default_mail_category = fields.Selection(
        selection=[
            ("SIMPLE", "Простое"),
            ("ORDERED", "Заказное"),
            ("ORDINARY", "Обыкновенное"),
            ("WITH_DECLARED_VALUE", "С объявленной ценностью"),
            (
                "WITH_DECLARED_VALUE_AND_CASH_ON_DELIVERY",
                "С объявленной ценностью и наложенным платежом",
            ),
        ],
        string="Категория отправления (Категория РПО)",
        default="WITH_DECLARED_VALUE",
        default_model="post.order",
    )

    default_post_attach_store = fields.Boolean(
        string="Store post attachment (True-db,False-query on server everytime",
        default="True",
        default_model="post.order",
    )

    company_id = fields.Many2one(
        "res.company", string="Company Authentication", default=_get_company
    )
    accessToken = fields.Char(
        string="Application Authentication Token",
        related="company_id.accessToken",
    )
    protocol = fields.Char(
        string="Protocol connection", related="company_id.protocol"
    )
    host = fields.Char(string="Address api request", related="company_id.host")

    def import_rus_post(self):
        """
        Импорт заказов по ид в настройках модуля, к сожалению закгрузка сразу всех заказов
        не реализовано апи почтой России, поэтому заказы импортируюся только ид как
        внутреннему так и внешнему (с сервера ПР)
        """
        # path = "/1.0/backlog/" +"3349"
        path = "/1.0/backlog/search?query=" + urllib.pathname2url("#3449")
        request_headers = {
            "Content-Type": "application/json",
            "Accept": "application/json;charset=UTF-8",
            "Authorization": "AccessToken "
            + self.env.user.company_id.accessToken,
            "X-User-Authorization": "Basic " + self.env.user.basicToken,
        }

        url = (
            self.env.user.company_id.protocol
            + self.env.user.company_id.host
            + path
        )

        response = requests.get(url, headers=request_headers)
        # json.loads (response.text)
        raise exceptions.ValidationError(response.text)


class AddToBatch(models.TransientModel):
    _name = "post.addtobatch"
    """
    Wizard добавления заказа к уже существующему пакету. Список пакетов создается из
    поиска всех заказов со статусом "к сдаче" и фильтрации по уникальным значениям
    пакетов. Таким образом в selection остается список пакетов без повторений. Дальше
    по нажатию на кнопку сначала заказ перемещается на сервере и если все удачно,
    также перемещается локально.
    """

    @api.model
    def _getListBranches(self):
        batches = self.env["post.order"].search([("state", "=", "surrender")])

        unique_batches = []
        for batch in batches:
            unique_batches.append(batch.id_package)
        unique_batches = list(set(unique_batches))

        return [(x, str(x)) for x in unique_batches]

    batch = fields.Selection(_getListBranches)

    # @api.multi
    def add_to_batch(self):
        for i in self:
            if not self._context.get("post_order_ids", False):
                raise exceptions.ValidationError(
                    "Не найден заказ который необходимо добавить!"
                )

            request_headers = {
                "Content-Type": "application/json",
                "Accept": "application/json;charset=UTF-8",
                "Authorization": "AccessToken "
                + self.env.user.company_id.accessToken,
                "X-User-Authorization": "Basic " + self.env.user.basicToken,
            }
            path = "/1.0/batch/" + i.batch + "/shipment"

            for j in self._context["post_order_ids"]:
                # raise exceptions.ValidationError(j)
                order_obj = self.env["post.order"].browse(j)
                shipment_ids = [order_obj.id_post]

                url = (
                    self.env.user.company_id.protocol
                    + self.env.user.company_id.host
                    + path
                )

                response = requests.post(
                    url, headers=request_headers, data=json.dumps(shipment_ids)
                )

                # if response.status_code == 200:
                order_obj.write(
                    {
                        "response": response.text
                        + "/n TO SURRENDER OK and BATCH "
                        + i.batch,
                        "state": "surrender",
                        "id_package": i.batch,
                    }
                )
                # raise exceptions.ValidationError(j)
                # else:
                #    i.response = response.text + "/n TO SURRENDER BAD and BATCH" + i.batch

        return {
            "type": "ir.actions.act_window_close",
        }


class post_order(models.Model):
    """
    Модель данных почты России, реализованы основные обьекты и функции
    для работы с апи ПР
    """

    _name = "post.order"

    # @api.multi
    def name_get(self):
        return [
            (r.id, "%s" % (r.recipient_name + " " + r.id_post))
            for r in self
            if (r.recipient_name and r.id_post)
        ]

    def _get_request_headers(self):
        """
        return request headers with company access token and current user basic token
        """
        if not self.env.user.company_id.accessToken:
            raise exceptions.ValidationError(
                "У текущей компании пустое поле ключа доступа к ПР"
            )
        if not self.env.user.basicToken:
            raise exceptions.ValidationError(
                "У текущего пользователя пустое поле ключа доступ к ПР"
            )

        return {
            "Content-Type": "application/json",
            "Accept": "application/json;charset=UTF-8",
            "Authorization": "AccessToken "
            + self.env.user.company_id.accessToken,
            "X-User-Authorization": "Basic " + self.env.user.basicToken,
        }

    def _get_error_sync_string(self, field_name):
        """
        return string error for sync check
        """
        return '<p style="color:#8B0000">&#x2717; BAD: ' + field_name + " </p>"

    # @api.multi
    def _clear_address(self):
        """
        Set value '' (clear) in all fields of address
        """
        for part_addr in [
            "street",
            "house",
            "slash",
            "letter",
            "corpus",
            "building",
            "room",
            "hotel",
            "num_address_type",
            "region",
            "area",
            "location",
            "place",
        ]:
            setattr(self, part_addr, "")

    # @api.multi
    def _check_sync(self):
        """
        Func find in PoR order with our order_num.name and compare ALL fields
        if one of fields dont compare sync is BAD
        """
        for i in self:
            if not i.sale_order_id or not i.id_post:
                i.status_sync = self._get_error_sync_string(
                    "sale_order_id.name or id_post empty"
                )
                continue
            # 2 type search in new orders and surrender orders
            if i.state == "new":
                path = "/1.0/backlog/search?query=" + urllib.pathname2url(
                    i.sale_order_id.name
                )
            else:
                path = "/1.0/shipment/" + i.id_post

            request_headers = self._get_request_headers()
            url = (
                self.env.user.company_id.protocol
                + self.env.user.company_id.host
                + path
            )
            response = requests.get(url, headers=request_headers)

            if i.state == "new":
                # if response == [ ] is a empty list, with size char 3 == not found by name
                if len(response.text) < 4:
                    i.status_sync = self._get_error_sync_string(
                        "sale_order_id.name not found in PoR"
                    )
                    i.response = response.text
                    continue
                # if token limit request check, because response more then 3 size
                try:
                    jtext = json.loads(response.text)[0]
                except:
                    i.response = response.text
                    i.status_sync = self._get_error_sync_string("limit token")
                    continue
            else:
                jtext = json.loads(response.text)
                # if response with error him size = 3, else good response
                if len(jtext) < 4:
                    i.status_sync = self._get_error_sync_string(
                        "sale_order_id.name not found in PoR"
                    )
                    i.response = response.text
                    continue

            i.status_sync = '<p style="color:#006400"> &#x2713; OK  </p>'
            # Если не сходится заказ с сервера почты россии и в базе оду хоть по 1 полю пишем нет синхронизации
            for part_addr, val in jtext.items():
                if part_addr in [
                    "street-to",
                    "house-to",
                    "slash-to",
                    "letter-to",
                    "corpus-to",
                    "building-to",
                    "room-to",
                    "hotel-to",
                    "num_address_type-to",
                    "region-to",
                    "area-to",
                    "location-to",
                    "place-to",
                    "index-to",
                ]:
                    value = getattr(self, part_addr[0:-3])
                    if part_addr == "index-to":
                        if str(jtext[part_addr]) != str(value):
                            i.status_sync = self._get_error_sync_string(
                                part_addr
                            )
                            break
                    else:
                        if jtext[part_addr] != value:
                            i.status_sync = self._get_error_sync_string(
                                part_addr
                            )
                            break
                if part_addr in ["mass", "payment"]:
                    if str(jtext[part_addr]) != str(getattr(self, part_addr)):
                        i.status_sync = self._get_error_sync_string(part_addr)
                        break
                        # ,'list-number-date'
                if part_addr in [
                    "mail-type",
                    "tel-address",
                    "mail-category",
                    "insr-value",
                    "recipient-name",
                    "list-number-date",
                ]:
                    # try:
                    value = getattr(self, part_addr.replace("-", "_"))
                    if value:
                        if part_addr == "tel-address":
                            if str(jtext[part_addr])[1:] != str(value)[1:]:
                                i.status_sync = self._get_error_sync_string(
                                    part_addr
                                )
                                break
                        elif part_addr == "insr-value":
                            if int(jtext[part_addr]) != int(value):
                                i.status_sync = self._get_error_sync_string(
                                    part_addr
                                )
                                break
                        elif part_addr == "list-number-date":
                            if str(jtext[part_addr]) != str(value):
                                i.status_sync = self._get_error_sync_string(
                                    part_addr
                                )
                                break
                        else:
                            if jtext[part_addr] != value:
                                # raise exceptions.ValidationError("!"+jtext[part_addr]+"!"+value+"!")
                                i.status_sync = self._get_error_sync_string(
                                    part_addr
                                )
                                break
                # except:
                #    raise exceptions.ValidationError(getattr(self, part_addr.replace('-','_')))
                if part_addr == "id":
                    if str(jtext[part_addr]) != str(self.id_post):
                        i.status_sync = self._get_error_sync_string("id_post")
                        continue
                if part_addr == "order-num":
                    if jtext[part_addr] != self.sale_order_id.name:
                        i.status_sync = self._get_error_sync_string("order_num")
                        continue

    # @api.multi
    def _concact_address(self):
        """
        Возвращаем конкатенированный адрес, аналогичный интерфейсу на сайте почты России
        """
        for i in self:
            address_format = "%(index)s%(region)s%(area)s%(location)s%(place)s%(street)s%(house)s\
%(slash)s%(letter)s%(corpus)s%(building)s%(room)s%(hotel)s%(num_address_type)s"
            args = {
                "index": i.index + " " if i.index else "",
                "street": i.street + " " if i.street else "",
                "house": i.house + " " if i.house else "",
                "slash": i.slash + " " if i.slash else "",
                "letter": i.letter + " " if i.letter else "",
                "corpus": i.corpus + " " if i.corpus else "",
                "building": i.building + " " if i.building else "",
                "room": i.room + " " if i.room else "",
                "hotel": i.hotel + " " if i.hotel else "",
                "num_address_type": i.num_address_type + " "
                if i.num_address_type
                else "",
                "region": i.region + " " if i.region else "",
                "location": i.location + " " if i.location else "",
                "place": i.place + " " if i.place else "",
                "area": i.area + " " if i.area else "",
            }
            i.address = address_format % args

    response = fields.Text(string="Сырой ответ от сервера")
    address_success = fields.Html(
        string="Статус адреса",
        help="""Статус после нормализации адреса,
                                    должен быть выделен зеленым цветом, тогда адрес считается
                                    пригодным для отправки и может быть использован, если же
                                    выделен красным цветом, то необходимо изменить адрес или
                                    ввести вручную, к примеру не указания номера дома является
                                    пригодным адресом если подсвечен зеленым
                                    Для разработчика:
                                    Address success status display""",
    )
    address_success_store = fields.Html(
        string="Статус адреса", help="Address success status store"
    )

    # post side
    recipient_name = fields.Char(string="ФИО получателя")
    tel_address = fields.Char(string="Телефон получателя")
    address = fields.Char(
        string="Адрес получателя",
        help="Нормализуется автоматически после того как курсор переведен на другйо обьект",
    )
    id_post = fields.Char(
        string="Ид заказа в почте России",
        help="Ид заказа на сервере почты России, НЕ внутренний ид",
    )
    id_package = fields.Char(string="Ид пакета на почте Россиии")
    original_address = fields.Char(
        string="Оригинальный адрес",
        help="""Адрес, который был изначально введен в изначальном
                                     формате и возвращен обратно сервером, служит исключительно
                                     в информативных целях и целях контроля, в частности для
                                     проверки того, что вводил оператор""",
    )
    index = fields.Char(
        string="Индекс", help="Zip code (index) from post of Russia"
    )
    list_number_date = fields.Date(string="Дата документа для сдачи партии")
    date_start = fields.Date(
        string="Дата начала для календаря", default=fields.Date.today
    )
    postoffice_code = fields.Char(string="Индекс места приема")
    postoffice_address = fields.Char(string="Адрес места приема")
    postoffice_name = fields.Char(string="Наименование места приема")
    mail_type = fields.Selection(
        string="Тип отправления (Вид РПО)",
        selection=[
            ("POSTAL_PARCEL", 'Посылка "нестандартная"'),
            ("ONLINE_PARCEL", 'Посылка "онлайн"'),
            ("ONLINE_COURIER", 'Курьер "онлайн"'),
            ("EMS", "Отправление EMS"),
            ("EMS_OPTIMAL", "EMS оптимальное"),
            ("LETTER", "Письмо"),
            ("BANDEROL", "Бандероль"),
            ("BUSINESS_COURIER", "Бизнес курьер"),
            ("BUSINESS_COURIER_ES", "Бизнес курьер экпресс"),
            ("PARCEL_CLASS_1", "Посылка 1-го класса"),
        ],
    )
    mail_category = fields.Selection(
        string="Категория отправления (Категория РПО)",
        selection=[
            ("SIMPLE", "Простое"),
            ("ORDERED", "Заказное"),
            ("ORDINARY", "Обыкновенное"),
            ("WITH_DECLARED_VALUE", "С объявленной ценностью"),
            (
                "WITH_DECLARED_VALUE_AND_CASH_ON_DELIVERY",
                "С объявленной ценностью и наложенным платежом",
            ),
        ],
    )
    transport_type = fields.Selection(
        string="Вид транспортировки",
        selection=[
            ("SURFACE", "Наземный"),
            ("AVIA", "Авиа"),
            ("COMBINED", "Комбинированный"),
            ("EXPRESS", "Системой ускоренной почты"),
        ],
    )
    payment_method = fields.Selection(
        string="Способы оплаты",
        selection=[
            ("CASHLESS", "Безналичный расчет"),
            ("STAMP", "Оплата марками"),
            ("FRANKING", "Франкирование"),
        ],
    )
    batch_status = fields.Selection(
        string="Статусы партии",
        selection=[
            ("CREATED", "Партия создана"),
            ("FINALIZED", "Партия финализирована"),
            (
                "SENT",
                "По заказам в партии существуют данные в сервисе трекинга",
            ),
            ("COMPLETED", "Все заказы партии отправлены"),
            ("ARCHIVED", "Партия находится в архиве"),
            ("DELETED", "Партия удалена"),
        ],
    )

    brand_name = fields.Char(string="Brand name")
    mass = fields.Char(string="Вес в граммах, включая упаковку", default="1")
    insr_value = fields.Integer(string="Сумма объявленной ценности (копейки)")
    payment = fields.Integer(string="Сумма наложенного платежа (копейки)")
    sale_order_id = fields.Many2one(
        "sale.order",
        string="Внутренний номер отправления",
        help="""Не путать с номер ид заказа на почте России.
                                        Это номер заказа  в магазине. По умолчанию берется
                                        имя/номер ордера продаж из модуля sale""",
    )
    delivery_order_id = fields.Many2one(
        "stock.picking", string="Номер ордера доставки"
    )
    state = fields.Selection(
        string="Статус заказа",
        selection=[
            ("new", "Новые"),
            ("surrender", "К сдаче"),
            ("archive", "Архив"),
        ],
        default="new",
    )
    status_sync = fields.Html(
        compute=_check_sync,
        string="Синхронизация",
        help="""Статус синхронизации - означает совпадение данных на сервере почты России и в системе оду,
                                 Должен подсвечиваться зеленым. Если одно из полей, например вес посылки или имя отправителя НЕ
                                 совпадает с полем такого же заказа (проверяется по ид заказа магазина) на сервере ПР то выдается ошибка""",
    )
    # status_sync_store = fields.Html(string=u"Синхронизация",compute=_check_sync_get_store)
    post_attach_store = fields.Boolean(
        string="Store post attachment (True-db,False-query on server everytime"
    )

    # Адрес улица
    street = fields.Char(string="Часть адреса: Улица опц")
    house = fields.Char(string="Часть адреса: Номер здания опц")
    slash = fields.Char(string="Часть здания: Дробь опц")
    letter = fields.Char(string="Часть здания: Литера опц")
    corpus = fields.Char(string="Часть здания: Корпус опц")
    building = fields.Char(string="Часть здания: Строение опц")
    room = fields.Char(string="Часть здания: Номер помещения опц")
    hotel = fields.Char(string="Название гостиницы опц")
    num_address_type = fields.Char(
        string="Номер для а/я, войсковая часть, войсковая часть ЮЯ, полевая почта"
    )

    # Адрес город
    region = fields.Char(string="Область, регион")
    area = fields.Char(string="Район опц")
    location = fields.Char(string="Микрорайон опц")
    place = fields.Char(string="Населенный пункт")

    # @api.multi
    def create_order_post(self):
        # raise exceptions.ValidationError(self)
        for i in self:
            # raise exceptions.ValidationError(i)
            path = "/1.0/user/backlog"
            request_headers = self._get_request_headers()
            url = (
                self.env.user.company_id.protocol
                + self.env.user.company_id.host
                + path
            )
            post_order_data = {
                # "brand-name": res.brand_name,
                "address-type-to": "DEFAULT",
                "index-to": i.index,
                "mail-category": i.mail_category,
                "mail-direct": 643,
                "mail-type": i.mail_type,
                "mass": i.mass,
                "order-num": i.sale_order_id.name,
                "place-to": i.place,
                "region-to": i.region,
                "street-to": i.street,
                "house-to": i.house,
                "tel-address": i.tel_address,
                "manual-address-input": "false",
                "insr-value": i.insr_value,
                # "payment": i.payment,
                # "payment-method": i.payment_method,
                "recipient-name": i.recipient_name,
            }
            if i.mail_category == "WITH_DECLARED_VALUE_AND_CASH_ON_DELIVERY":
                post_order_data["payment"] = i.payment
                # raise exceptions.ValidationError(i.payment)
            new_orders = [
                post_order_data,
            ]
            response = requests.put(
                url, headers=request_headers, data=json.dumps(new_orders)
            )
            # пока создаем только один заказ
            i.response = response.text
            jtext = json.loads(response.text)
            if jtext.get("result-ids", False):
                for ids in jtext["result-ids"]:
                    i.id_post = ids

    @api.model
    def create(self, vals):
        if vals.get("address_success_store", False):
            vals["address_success"] = vals["address_success_store"]
        res = super().create(vals)
        self = res
        self.normalize_addr()
        self.create_order_post()
        if not res.id_post:
            raise exceptions.ValidationError(res.response)
        return res

    # @api.multi
    def write(self, vals):
        if vals.get("address_success_store", False):
            vals["address_success"] = vals["address_success_store"]
        # Save our change in our local base!
        res = super().write(vals)
        for i in self:
            if not i.id_post:
                continue
            request_headers = self._get_request_headers()
            if vals.get("list_number_date", False) and i.id_package:
                date = fields.Date.from_string(i.list_number_date)
                # date = fields.Date.from_string(vals.get('list_number_date', False))
                path = (
                    "/1.0/batch/"
                    + i.id_package
                    + "/sending/"
                    + str(date.year)
                    + "/"
                    + str(date.month)
                    + "/"
                    + str(date.day)
                )
                url = (
                    self.env.user.company_id.protocol
                    + self.env.user.company_id.host
                    + path
                )
                # raise exceptions.ValidationError(url)
                response = requests.post(url, headers=request_headers)

            shipment_id = i.id_post
            shipment_update = {
                "address-type-to": "DEFAULT",
                # "dimension" : {
                #   "height" : 22,
                #   "length" : 20,
                #   "width" : 21
                # },
                # "fragile": "false",
                "given-name": i.recipient_name,
                "num_address_type-to": i.num_address_type,
                "index-to": i.index,
                "insr-value": i.insr_value,
                "mail-category": i.mail_category,
                "mail-type": i.mail_type,
                "mass": i.mass,
                "order-num": i.sale_order_id.name,
                "payment": i.payment,
                "tel-address": i.tel_address,
            }
            for part_addr in [
                "street",
                "house",
                "slash",
                "letter",
                "corpus",
                "building",
                "room",
                "hotel",
                "num_address_type",
                "region",
                "area",
                "location",
                "place",
            ]:
                if getattr(self, part_addr):
                    shipment_update[part_addr + "-to"] = getattr(
                        self, part_addr
                    )

            path = "/1.0/backlog/" + shipment_id
            url = (
                self.env.user.company_id.protocol
                + self.env.user.company_id.host
                + path
            )
            response = requests.put(
                url, headers=request_headers, data=json.dumps(shipment_update)
            )

            # download zip with documents
            if i.id_package and i.state != "new":
                self.document_to_attachment(
                    i.id_package, i.id_post, self.id, "post.order"
                )
        # Save response!
        res = super().write(vals)
        return res

    # @api.multi
    def document_to_attachment(self, id_package, id_post, res_id, model_name):
        if id_package and id_post:
            url = (
                self.env.user.company_id.protocol
                + self.env.user.company_id.host
                + "/1.0/forms/"
                + id_package
                + "/zip-all"
            )
            type_attach = "binary"
            file_bin = ""
            # 2 type store file url and local
            if self.post_attach_store:
                type_attach = "binary"
                response = requests.get(
                    url, headers=self._get_request_headers(), stream=True
                )
                for block in response.iter_content(1024):
                    file_bin += block
            else:
                type_attach = "url"

            attach_ids = self.env["ir.attachment"].search(
                [
                    (
                        "name",
                        "=",
                        "Скачать архивом "
                        + type_attach
                        + str(id_post).decode("utf-8"),
                    ),
                    ("type", "=", type_attach),
                    ("res_id", "=", res_id),
                    ("res_model", "=", model_name),
                ],
                limit=1,
            )
            if not attach_ids:
                attachment = {
                    "name": "Скачать архивом "
                    + type_attach
                    + str(id_post).decode("utf-8"),
                    "type": type_attach,
                    "user_id": self.env.user.id,
                    "res_id": res_id,
                    "res_model": model_name,
                }
                attach_ids = self.env["ir.attachment"].create(attachment)
            for attach_id in attach_ids:
                attach_obj = self.env["ir.attachment"].browse(attach_id.id)
                if self.post_attach_store:
                    attach_obj.datas = base64.b64encode(file_bin)
                    attach_obj.datas_fname = "forms_all_" + id_package + ".zip"
                    attach_obj.description = "post_rus"
                else:
                    # call controller and download file on request lib on fly, dont store file in DB
                    attach_obj.url = (
                        "web/content/" + str(attach_id.id) + "?download=True"
                    )
                    attach_obj.datas_fname = "forms_all_" + id_package + ".zip"
                    attach_obj.description = (
                        "post_rus!"
                        + self.env.user.company_id.accessToken
                        + "!"
                        + self.env.user.basicToken
                        + "!"
                        + url
                    )

    # @api.multi
    def merger_pdf(self):
        for rec in self:
            type_attach = "binary" if rec.post_attach_store else "url"

            attach_ids = self.env["ir.attachment"].search(
                [
                    (
                        "name",
                        "=",
                        "Скачать архивом "
                        + type_attach
                        + str(rec.id_post).decode("utf-8"),
                    ),
                    ("type", "=", type_attach),
                    ("res_id", "=", rec.id),
                    ("res_model", "=", self._name),
                ],
                limit=1,
            )
            for attach_id in attach_ids:
                attach_obj = self.env["ir.attachment"].browse(attach_id.id)
                file_bin = ""
                if type_attach == "binary":
                    file_bin = base64.b64decode(attach_obj.datas)
                else:
                    url = (
                        self.env.user.company_id.protocol
                        + self.env.user.company_id.host
                        + "/1.0/forms/"
                        + rec.id_package
                        + "/zip-all"
                    )
                    response = requests.get(
                        url, headers=self._get_request_headers(), stream=True
                    )
                    for block in response.iter_content(1024):
                        file_bin += block

                archive = zipfile.ZipFile(io.BytesIO(file_bin))
                doc_pdf = False
                if (
                    rec.mail_category
                    == "WITH_DECLARED_VALUE_AND_CASH_ON_DELIVERY"
                ):
                    if rec.mail_type == "EMS":
                        doc_pdf = archive.read("F_EMS_F112.pdf")
                    else:
                        doc_pdf = archive.read("F7_F112.pdf")
                else:
                    doc_pdf = archive.read("F7.pdf")
                doc_pdf2 = archive.read("F103.pdf")
                doc_csv = archive.read("EXPORT.csv")

                attachment = {
                    "name": "Скачать файл для печати "
                    + str(rec.id_post).decode("utf-8"),
                    "type": "binary",
                    "user_id": self.env.user.id,
                    "res_id": rec.id,
                    "res_model": self._name,
                }
                merger_attachment = self.env["ir.attachment"].create(attachment)

                packet = StringIO()
                can = canvas.Canvas(packet, pagesize=landscape(A4))
                csv_file = csv.reader(io.BytesIO(doc_csv), delimiter=",")
                y = 550
                for line in csv_file:
                    can.drawString(
                        30, y, ",".join(str(x).decode("utf-8") for x in line)
                    )
                    y -= 10
                can.save()
                packet.seek(0)

                # move to the beginning of the StringIO buffer
                merger = PdfFileMerger()
                if doc_pdf:
                    input1 = PdfFileReader(io.BytesIO(doc_pdf))
                    merger.append(input1)
                input2 = PdfFileReader(io.BytesIO(doc_pdf2))
                new_pdf = PdfFileReader(packet)

                # merger.append(input1)
                merger.append(input2)
                merger.append(new_pdf)

                myio = StringIO()
                merger.write(myio)
                merger_attachment.datas = base64.b64encode(myio.getvalue())
                merger_attachment.datas_fname = (
                    "merge_from_zip_" + str(rec.id_post) + ".pdf"
                )

                packet.close()
                myio.close()
                merger.close()

    # @api.multi
    def unlink(self):
        for i in self:
            if not i.id_post:
                continue
            request_headers = self._get_request_headers()
            path = "/1.0/backlog"
            backlog_ids = [i.id_post]
            url = (
                self.env.user.company_id.protocol
                + self.env.user.company_id.host
                + path
            )
            response = requests.delete(
                url, headers=request_headers, data=json.dumps(backlog_ids)
            )
        return super().unlink()

    # @api.multi
    def to_new(self):
        for i in self:
            if not i.id_post:
                raise exceptions.ValidationError(
                    "Ид заказа отсутствует!Возможно заказ не создан на сервере почты России(к новым)"
                )
            request_headers = self._get_request_headers()

            path = "/1.0/user/backlog"

            shipments_to_backlogs = [i.id_post]

            url = (
                self.env.user.company_id.protocol
                + self.env.user.company_id.host
                + path
            )

            response = requests.post(
                url,
                headers=request_headers,
                data=json.dumps(shipments_to_backlogs),
            )
            if response.status_code == 200:
                i.write(
                    {
                        "response": response.text + "/n TO NEW OK",
                        "state": "new",
                        "id_package": False,
                    }
                )
            else:
                i.response = response.text + "/n TO NEW BAD"

    # @api.multi
    def checkin(self, id_package):
        path = "/1.0/batch/" + str(id_package) + "/checkin"
        url = (
            self.env.user.company_id.protocol
            + self.env.user.company_id.host
            + path
        )
        response = requests.post(url, headers=self._get_request_headers())

    # @api.multi
    def to_surrender(self):
        for i in self:
            if not i.id_post:
                raise exceptions.ValidationError(
                    "Ид заказа отсутствует!Возможно заказ не создан на сервере почты России(к сдаче)"
                )
            if i.id_package:
                self.checkin(i.id_package)
            else:
                path = "/1.0/user/shipment"
                shipment_ids = [i.id_post]
                url = (
                    self.env.user.company_id.protocol
                    + self.env.user.company_id.host
                    + path
                )
                response = requests.post(
                    url,
                    headers=self._get_request_headers(),
                    data=json.dumps(shipment_ids),
                )

                jtext = ""
                if response.status_code == 200:
                    # берем данные из batches
                    try:
                        jtext = json.loads(response.text)
                    except:
                        raise exceptions.ValidationError(jtext)

                    batches = jtext.get("batches", False)
                    if batches:
                        batch_first = batches[0]
                        i.write(
                            {
                                "response": response.text,
                                "state": "surrender",
                                "id_package": batch_first.get(
                                    "batch-name", False
                                ),
                                "transport_type": batch_first.get(
                                    "transport-type", False
                                ),
                                "payment_method": batch_first.get(
                                    "payment-method", False
                                ),
                                "batch_status": batch_first.get(
                                    "batch-status", False
                                ),
                                "postoffice_code": batch_first.get(
                                    "postoffice-code", False
                                ),
                                "postoffice_address": batch_first.get(
                                    "postoffice-address", False
                                ),
                                "postoffice_name": batch_first.get(
                                    "postoffice-name", False
                                ),
                                #'list_number_date': fields.Date.from_string(batch_first.get('list-number-date',False)),
                                "list_number_date": batch_first.get(
                                    "list-number-date", False
                                ),
                            }
                        )
                        self.checkin(batch_first.get("batch-name", False))
                else:
                    i.response = response.text + "/n TO SURRENDER BAD"

    # @api.multi
    def to_archive(self):
        for i in self:
            if not i.id_package:
                raise exceptions.ValidationError(
                    "Ид заказа отсутствует!Возможно заказ не создан на сервере почты России(в архив)"
                )
            request_headers = self._get_request_headers()

            path = "/1.0/archive"

            batches_to_archive = [i.id_package]

            url = (
                self.env.user.company_id.protocol
                + self.env.user.company_id.host
                + path
            )

            response = requests.put(
                url,
                headers=request_headers,
                data=json.dumps(batches_to_archive),
            )
            if response.status_code == 200:
                i.write(
                    {
                        "response": response.text + "/n TO ARCHIVE OK",
                        "state": "archive",
                    }
                )
            else:
                i.response = response.text + "/n TO ARCHIVE BAD"

    def parse_address(self, jtext):
        # save in DB all address fields from server
        for part_addr, val in jtext.items():
            if part_addr in [
                "street",
                "house",
                "slash",
                "letter",
                "corpus",
                "building",
                "room",
                "hotel",
                "num_address_type",
                "region",
                "area",
                "location",
                "place",
            ]:
                setattr(self, part_addr, val)

        # Номер для а/я, войсковая часть, войсковая часть ЮЯ, полевая почта
        self.num_address_type = jtext.get("num-address-type", False)
        self.index = jtext.get("index", False)
        self.original_address = jtext.get("original-addresse", False)
        self._concact_address()

    # @api.multi
    @api.onchange("address")
    def normalize_addr(self):
        path = "/1.0/clean/address"
        type_address = {
            "DEFAULT": "Стандартный (улица, дом, квартира)",
            "PO_BOX": "Абонентский ящик",
            "DEMAND": "До востребования",
        }

        good_cod_quality = ["GOOD", "POSTAL_BOX", "ON_DEMAND", "UNDEF_05"]
        cod_quality = {
            "GOOD": "Пригоден для почтовой рассылки",
            "ON_DEMAND": "До востребования",
            "POSTAL_BOX": "Абонентский ящик",
            "UNDEF_01": "Не определен регион",
            "UNDEF_02": "Не определен город или населенный пункт",
            "UNDEF_03": "Не определена улица",
            "UNDEF_04": "Не определен номер дома",
            "UNDEF_05": "Не определена квартира/офис",
            "UNDEF_06": "Не определен",
            "UNDEF_07": "Иностранный адрес",
        }
        good_cod_validation = ["VALIDATED", "OVERRIDDEN", "CONFIRMED_MANUALLY"]
        cod_validation = {
            "CONFIRMED_MANUALLY": "Подтверждено контролером",
            "VALIDATED": "Уверенное распознавание",
            "OVERRIDDEN": "Распознан: адрес был перезаписан в справочнике",
            "NOT_VALIDATED_HAS_UNPARSED_PARTS": "На проверку, неразобранные части",
            "NOT_VALIDATED_HAS_ASSUMPTION": "На проверку, предположение",
            "NOT_VALIDATED_HAS_NO_MAIN_POINTS": "На проверку, нет основных частей",
            "NOT_VALIDATED_HAS_NUMBER_STREET_ASSUMPTION": "На проверку, предположение по улице",
            "NOT_VALIDATED_HAS_NO_KLADR_RECORD": "На проверку, нет в КЛАДР",
            "NOT_VALIDATED_HOUSE_WITHOUT_STREET_OR_NP": "На проверку, нет улицы или населенного пункта",
            "NOT_VALIDATED_HOUSE_EXTENSION_WITHOUT_HOUSE": "На проверку, нет дома",
            "NOT_VALIDATED_HAS_AMBI": "На проверку, неоднозначность",
            "NOT_VALIDATED_EXCEDED_HOUSE_NUMBER": "На проверку, большой номер дома",
            "NOT_VALIDATED_INCORRECT_HOUSE": "На проверку, некорректный дом",
            "NOT_VALIDATED_INCORRECT_HOUSE_EXTENSION": "На проверку, некорректное расширение дома",
            "NOT_VALIDATED_FOREIGN": "Иностранный адрес",
            "NOT_VALIDATED_DICTIONARY": "На проверку, не по справочнику",
        }
        request_headers = self._get_request_headers()
        self._clear_address()
        # setting = self.env['post.setting'].search([('1', '=', '1')])[0]
        # raise exceptions(setting)

        url = (
            self.env.user.company_id.protocol
            + self.env.user.company_id.host
            + path
        )

        data = [
            {
                "id": "adr 1",
                "original-address": self.address,  # "г. Москва, Варшавское шоссе, 37"
            },
        ]
        response = requests.post(
            url, data=json.dumps(data), headers=request_headers
        )

        # пока нормализуем только один адрес а раз
        try:
            jtext = json.loads(response.text)[0]
        except:
            raise exceptions.ValidationError(response.text)
        self.response = jtext
        self.address_success = ""
        quality_flag = False
        validation_flag = False

        # CHECK quality code
        if jtext["quality-code"] in good_cod_quality:
            self.address_success += (
                '<p style="color:#006400">Код качества подтвержден! '
                + cod_quality[jtext["quality-code"]]
                + "</p>"
            )
            quality_flag = True
        else:
            self.address_success += (
                '<p style="color:#8B0000">Код качества НЕ подтвержден! '
                + cod_quality[jtext["quality-code"]]
                + "</p>"
            )

        # CHECK validation code
        if jtext["validation-code"] in good_cod_validation:
            self.address_success += (
                '<p style="color:#006400">Код валидации подтвержден! '
                + cod_validation[jtext["validation-code"]]
                + "</p>"
            )
            validation_flag = True
        else:
            self.address_success += (
                '<p style="color:#8B0000">Код валидации НЕ подтвержден! '
                + cod_validation[jtext["validation-code"]]
                + "</p>"
            )

        if quality_flag and validation_flag:
            self.address_success += (
                '<p style="color:#006400">Адрес приемлем для доставки! </p>'
            )
            self.index = jtext["index"]
            self.original_address = jtext[
                "original-address"
            ]  # street place house region
            self.parse_address(jtext)
        else:
            self.index = "Not found"
        self.address_success_store = self.address_success
