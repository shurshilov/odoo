import logging
from datetime import datetime

import pymorphy2
from dateutil.relativedelta import relativedelta
from odoo import api, exceptions, fields, models

_logger = logging.getLogger(__name__)


class PartnerContractCustomer(models.Model):
    _name = "partner.contract.customer"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    def get_dateend(self):
        if self.date_start:
            six_months = fields.Datetime.from_string(
                self.date_start
            ) + relativedelta(months=+11)
        else:
            six_months = datetime.today() + relativedelta(months=+11)
        return fields.Datetime.to_string(six_months)

    name = fields.Char(string="Номер")
    date_start = fields.Date(
        string="Дата договора", required=True, default=fields.Datetime.now()
    )
    partner_id = fields.Many2one(
        "res.partner", string="Контрагент", required=True
    )
    company_id = fields.Many2one("res.company", string="Компания")
    name_print = fields.Char(string="Имя для печати", compute="_get_name_print")
    name_print1 = fields.Char(
        string="Имя для печати, И.П.", compute="_get_name_printip"
    )
    date_end = fields.Date(
        string="Дата окончания", required=True, default=get_dateend
    )
    name_dirprint = fields.Char(
        string="Имя нашего директора для печати", compute="_get_name_print1"
    )
    name_dirprint1 = fields.Char(
        string="Имя нашего директора для печати И.П.",
        compute="_get_name_print1ip",
    )
    lines = fields.One2many(
        "contract.line", "contract_id", string="Договорные цены"
    )
    type = fields.Selection(
        [
            ("customer", "С клиентом"),
            ("supplier", "С подрядчиком"),
            ("transport", "На перевозку"),
        ],
        string="Тип договора",
        default="customer",
        required=1,
    )
    saleorder_id = fields.Many2one("sale.order", string="Заказ/Сделка")
    stamp = fields.Boolean(string="Печать и подпись")
    signed = fields.Boolean(string="Договор подписан")

    @api.model_create_multi
    def create(self, vals):
        result = super().create(vals)
        if result.partner_id.company_type == "person":
            result.signed = True
        return result

    def _get_name_print(self):
        morph = pymorphy2.MorphAnalyzer()
        self.name_print = ""
        director = self.env["res.partner"].search(
            [("parent_id", "=", self.partner_id.id), ("type", "=", "director")],
            limit=1,
        )
        if director:
            if not director.name:
                raise exceptions.UserError(
                    "Имя директора пустое!Пожалуйста, введите имя директора контрагента!"
                )
            if len(director.name.split(" ")) == 3:
                (
                    lastname_old,
                    firstname_old,
                    middlename_old,
                ) = director.name.split(" ")

                # _logger.warning('Старая функция склонения')
                if lastname_old:
                    lastname_n = morph.parse(lastname_old)[0]
                    if lastname_n.inflect({"gent"}):
                        try:
                            lastname_n = lastname_n.inflect({"gent"}).word
                        except:
                            lastname_n = lastname_old
                    else:
                        lastname_n = lastname_old
                else:
                    lastname_n = ""

                if firstname_old:
                    firstname_n = morph.parse(firstname_old)[0]
                    try:
                        firstname_n = firstname_n.inflect({"gent"}).word
                    except:
                        firstname_n = firstname_old
                else:
                    firstname_n = ""

                if middlename_old:
                    middlename_n = morph.parse(middlename_old)[0]
                    try:
                        middlename_n = middlename_n.inflect({"gent"}).word
                    except:
                        middlename_n = middlename_old
                else:
                    middlename_n = ""

                # _logger.warning('Новая функция склонения')
                ru_dict = morph._units[0][0].dict
                for idx, obj in enumerate(morph.parse(lastname_old)):
                    if obj.tag.POS == "NOUN":
                        if morph.parse(lastname_old)[idx].tag.gender == "femn":
                            if len(
                                morph.parse(lastname_old)[idx].normal_form
                            ) == len(lastname_old):
                                continue
                        break
                try:
                    paradigm_lastname = ru_dict.build_paradigm_info(
                        morph.parse(lastname_old)[idx][4][0][2]
                    )
                    paradigm_middlename = ru_dict.build_paradigm_info(
                        morph.parse(middlename_old)[0][4][0][2]
                    )
                    case = [
                        "Именительный",
                        "Родительный",
                        "Дательный",
                        "Винительный",
                        "Творительный",
                        "Предложный",
                    ]
                    case1 = [
                        "nomn",
                        "gent",
                        "datv",
                        "accs",
                        "ablt",
                        "loct",
                    ]
                    last_word_gent = lastname_old
                    first_word_gent = firstname_old
                    middle_word_gent = middlename_old
                    last_word_datv = lastname_old
                    first_word_datv = firstname_old
                    middle_word_datv = middlename_old
                    # Родительный падеж
                    for last_prefix, last_tag, last_suffix in paradigm_lastname:
                        if (
                            last_tag.gender
                            == morph.parse(firstname_old)[0].tag.gender
                            and last_tag.case == case1[1]
                        ):
                            if (
                                morph.parse(firstname_old)[0].tag.gender
                                == "femn"
                            ):
                                last_word_gent = (
                                    last_prefix
                                    + morph.parse(lastname_old)[idx].normal_form
                                    + last_suffix
                                )
                            else:
                                last_word_gent = (
                                    last_prefix
                                    + morph.parse(lastname_old)[idx][0]
                                    + last_suffix
                                )
                            break
                    for (
                        middle_prefix,
                        middle_tag,
                        middle_suffix,
                    ) in paradigm_middlename:
                        if (
                            middle_tag.gender
                            == morph.parse(firstname_old)[0].tag.gender
                            and middle_tag.case == case1[1]
                            and not middle_tag._str.endswith("Erro")
                            and not middle_tag._str.endswith("V-ie")
                        ):
                            if (
                                morph.parse(firstname_old)[0].tag.gender
                                == "femn"
                            ):
                                middle_word_gent = (
                                    middle_prefix
                                    + middlename_old[: -1 * len(middle_suffix)]
                                    + middle_suffix
                                )
                            else:
                                middle_word_gent = (
                                    middle_prefix
                                    + middlename_old[
                                        : -1 * (len(middle_suffix) - 1)
                                    ]
                                    + middle_suffix
                                )
                            break
                    first_word_gent = morph.parse(firstname_old)[0].inflect(
                        {case1[1]}
                    )[0]
                    name_print_gent = (
                        last_word_gent.capitalize()
                        + " "
                        + first_word_gent.capitalize()
                        + " "
                        + middle_word_gent.capitalize()
                    )
                    _logger.warning(case[1] + ": " + name_print_gent)
                    # Дательный падеж
                    for last_prefix, last_tag, last_suffix in paradigm_lastname:
                        if (
                            last_tag.gender
                            == morph.parse(firstname_old)[0].tag.gender
                            and last_tag.case == case1[2]
                        ):
                            if (
                                morph.parse(firstname_old)[0].tag.gender
                                == "femn"
                            ):
                                last_word_datv = (
                                    last_prefix
                                    + morph.parse(lastname_old)[idx].normal_form
                                    + last_suffix
                                )
                            else:
                                last_word_datv = (
                                    last_prefix
                                    + morph.parse(lastname_old)[idx][0]
                                    + last_suffix
                                )
                            break
                    for (
                        middle_prefix,
                        middle_tag,
                        middle_suffix,
                    ) in paradigm_middlename:
                        if (
                            middle_tag.gender
                            == morph.parse(firstname_old)[0].tag.gender
                            and middle_tag.case == case1[2]
                            and not middle_tag._str.endswith("Erro")
                            and not middle_tag._str.endswith("V-ie")
                        ):
                            if (
                                morph.parse(firstname_old)[0].tag.gender
                                == "femn"
                            ):
                                middle_word_datv = (
                                    middle_prefix
                                    + middlename_old[: -1 * len(middle_suffix)]
                                    + middle_suffix
                                )
                            else:
                                middle_word_datv = (
                                    middle_prefix
                                    + middlename_old[
                                        : -1 * (len(middle_suffix) - 1)
                                    ]
                                    + middle_suffix
                                )
                            break
                    first_word_datv = morph.parse(firstname_old)[0].inflect(
                        {case1[2]}
                    )[0]
                    name_print_datv = (
                        last_word_datv.capitalize()
                        + " "
                        + first_word_datv.capitalize()
                        + " "
                        + middle_word_datv.capitalize()
                    )
                    _logger.warning(case[2] + ": " + name_print_datv)

                    self.name_print = name_print_gent.title()
                except:
                    _logger.warning(
                        "ФИО директора имеет более 3 слов или более 2 пробелов! Склонение ФИО пропущено!"
                    )

    def _get_name_print1(self):
        for rec in self:
            morph = pymorphy2.MorphAnalyzer()
            director = rec.company_id.chief_id.partner_id
            rec.name_dirprint = ""
            if director:
                if not director.name:
                    raise exceptions.UserError(
                        "Имя директора пустое!Пожалуйста, введите имя директора контрагента!"
                    )
                if len(director.name.split(" ")) == 3:
                    (
                        lastname_old,
                        firstname_old,
                        middlename_old,
                    ) = director.name.split(" ")
                    if lastname_old == "Крюкова":
                        lastname_n = "Крюковой"
                    elif lastname_old:
                        lastname_n = morph.parse(lastname_old)[0]
                        lastname_n = lastname_n.inflect({"gent"}).word
                    else:
                        lastname_n = ""

                    if firstname_old:
                        firstname_n = morph.parse(firstname_old)[0]
                        firstname_n = firstname_n.inflect({"gent"}).word
                    else:
                        firstname_n = ""

                    if middlename_old:
                        middlename_n = morph.parse(middlename_old)[0]
                        middlename_n = middlename_n.inflect({"gent"}).word
                    else:
                        middlename_n = ""
                    name_print = (
                        lastname_n + " " + firstname_n + " " + middlename_n
                    )
                    rec.name_dirprint = name_print.title()
                else:
                    _logger.warning(
                        "ФИО директора имеет более 3 слов или более 2 пробелов! Склонение ФИО пропущено!"
                    )

    @api.model_create_multi
    def create(self, values):
        res = super().create(values)
        if self.partner_id.customer and not self.partner_id.supplier:
            sequence_code = "partner.contract.customer.sequence"
            name = self.env["ir.sequence"].next_by_code(sequence_code)
            res.update(
                {
                    "name": name,
                }
            )
        elif not self.partner_id.customer and self.partner_id.supplier:
            res = super().create(values)
            sequence_code = "partner.contract.supplier.sequence"
            name = self.env["ir.sequence"].next_by_code(sequence_code)
            res.update(
                {
                    "name": name,
                }
            )
        return res

    def _get_name_print1ip(self):
        for rec in self:
            rec.name_dirprint1 = rec.company_id.chief_id.partner_id.name

    def _get_name_printip(self):
        for rec in self:
            rec.name_print1 = ""
            director = self.env["res.partner"].search(
                [
                    ("parent_id", "=", rec.partner_id.id),
                    ("type", "=", "director"),
                ],
                limit=1,
            )
            if director:
                rec.name_print1 = director.name

    def print_transport(self):
        return self.env.ref(
            "mta_base.action_mtacontracttrans_report"
        ).report_action(self)

    def print_supp(self):
        return self.env.ref(
            "mta_base.action_mtacontractsupp_report"
        ).report_action(self)

    def print_contract_cust(self):
        if self.saleorder_id:
            return self.saleorder_id.print_contract()
        else:
            raise exceptions.UserError(
                "Вы не можете напечатать договор с Клиентом, потому что нет связи с Заказом. Нужно зайти в Заказ и привязать этот договор."
            )

    @api.onchange("name")
    def set_comp_and_partn(self):
        order_id = self._context.get("sale_order_id")
        if order_id:
            sale_order = self.env["sale.order"].browse(order_id)
            self.company_id = sale_order.company_id
            self.partner_id = sale_order.partner_id


class Partner(models.Model):
    _inherit = "res.partner"

    customer = fields.Boolean(
        string="Это клиент",
        default=True,
        help="Check this box if this contact is a customer. It can be selected in sales orders.",
    )
    supplier = fields.Boolean(
        string="Это поставщик",
        help="Check this box if this contact is a vendor. It can be selected in purchase orders.",
    )
    contract_count = fields.Integer(
        string="Договора", compute="get_count_contract"
    )
    partner_contract_ids = fields.One2many(
        "partner.contract.customer", "partner_id", string="Договора"
    )
    pol = fields.Selection(
        string="Пол",
        selection=[
            ("m", "Муж."),
            ("j", "Жен"),
        ],
        required=False,
    )

    def get_count_contract(self):
        for rec in self:
            contract = self.env["partner.contract.customer"]
            rec.contract_count = contract.search_count(
                [("partner_id", "=", rec.id), ("signed", "=", True)]
            )

    def action_view_contract(self):
        self.ensure_one()
        view = self.env.context.get("view")
        if view:
            res = self.env["ir.actions.act_window"]._for_xml_id(view)
            res.update(
                context=dict(
                    self.env.context, default_partner_id=self.id, group_by=False
                ),
                domain=[("partner_id", "=", self.id)],
            )
            return res
        return False


class ContractLine(models.Model):
    _name = "contract.line"
    contract_id = fields.Many2one(
        "partner.contract.customer",
        string="Order Reference",
        required=True,
        ondelete="cascade",
        index=True,
        copy=False,
    )
    name = fields.Text(string="Название для договора", required=True)
    price_unit = fields.Float("Цена", required=True, default=0.0)
    product_uom = fields.Many2one(
        "uom.uom", string="Единица измерения", required=True
    )
    product_id = fields.Many2one(
        "product.product",
        string="Услуга",
        domain=[("sale_ok", "=", True)],
        change_default=True,
        ondelete="restrict",
        required=True,
    )

    @api.onchange("product_id")
    def set_name(self):
        self.name = self.product_id.name
