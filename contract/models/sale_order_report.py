from datetime import datetime

from odoo import exceptions, fields, models

from .report_helper import Helper


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @staticmethod
    def format_partner(partner):
        result = []
        if partner.zip:
            result.append(partner.zip)
        if partner.city:
            result.append(partner.city)
        if partner.street:
            result.append(partner.street)
        return ", ".join(result) or ""

    def get_report_sale_order_context_rus(self):
        """Данные для счета на оплату для РФ.
        данная функция - пример настройки продакшена, но не забывайте
        что часть полей кастомная, например основание содержит камтомную модель
        договора.
        Все кастомные модели необходимо заменить на ваши или заккоментировать
        """
        self = self.sudo()
        # набор полезных функций, чтобы не засорять пространство sale.order
        helper = Helper()
        # сборка линий заказа, с учетом кастомной логики отработки
        order_line = []
        summ = 0
        summ_nds = 0
        for line in self.order_line:
            new_line = {}
            nds = 0.0
            if line.tax_id:
                nds = line.tax_id[0].amount / (100 + line.tax_id[0].amount)
            if line.product_uom_qty > 0:
                new_line["index"] = len(order_line) + 1
                new_line["name"] = line.name or ""
                new_line["qty"] = line.product_uom_qty or ""
                new_line["product_uom"] = line.product_uom.name or ""
                new_line["currency"] = "руб."
                new_line["price"] = line.price_unit or ""
                new_line["total_price"] = line.price_unit * (
                    line.product_uom_qty
                )
                summ = summ + line.price_unit * (line.product_uom_qty)
                summ_nds = (
                    summ_nds + line.price_unit * (line.product_uom_qty) * nds
                )
                order_line.append(new_line)

        return {
            # Банк получателя
            "bank_received": (
                self.company_id.partner_id.bank_ids
                and self.company_id.partner_id.bank_ids[0].bank_name
                or ""
            )
            + " "
            + (
                self.company_id.partner_id.bank_ids
                and self.company_id.partner_id.bank_ids[0].bank_id.city
                or ""
            ),
            # БИК
            "bik": self.company_id.partner_id.bank_ids
            and self.company_id.partner_id.bank_ids[0].bank_bic
            or "",
            # Р/Счёт №.
            "acc_number": self.company_id.partner_id.bank_ids
            and self.company_id.partner_id.bank_ids[0].acc_number
            or "",
            # ИНН
            "inn": self.company_id.inn or "",
            # RRGG
            "kpp": self.company_id.kpp or "",
            # К/ Счёт №
            "correspondent_account": self.company_id.partner_id.bank_ids
            and self.company_id.partner_id.bank_ids[
                0
            ].bank_id.correspondent_account
            or "",
            # Получатель
            "reciver": self.company_id.name or "",
            # номер счета
            "so_number": helper.numer(self.name)
            + "-"
            + str(datetime.today().month)
            + str(datetime.today().day),
            # от
            "so_from": helper.ru_date2(
                datetime.today().strftime("%Y-%m-%d %H:%M:%S")
            ),
            # поставщик
            "provider": helper.representation(self.company_id),
            # покупатель
            "customer": helper.representation(self.partner_id),
            # основание
            # 'contract': "Договор № " + self.mt_contractid.name +" от "+fields.Date.from_string(self.mt_contractid.date_start).strftime("%d.%m.%Y"),
            "manager": "Менеджер: "
            + self.user_id.name
            + ", email: "
            + self.user_id.partner_id.email
            or "" + ", тел. " + self.user_id.partner_id.mobile
            or "",
            "order_line": order_line,
            "len_order_line": len(order_line),
            "summ": summ or "0,00",
            "summ_nds": round(summ_nds, 2) or "0,00",
            "summ_text": helper.rubles(summ).capitalize(),
            "chief": helper.initials(self.company_id.chief_id.name),
            "accountant": helper.initials(self.company_id.accountant_id.name),
            # IMAGES
            # 1.jpg, 2.jpg, 3.jpg Печать и подпись берутся динамически из полей.
            "images": [
                self.company_id.chief_id.facsimile,
                self.company_id.accountant_id.facsimile,
                self.company_id.stamp,
            ],
        }

    def get_report_sale_order_context(self):
        """Пример данных для договора"""
        self = self.sudo()
        if not self.mt_contractid:
            raise exceptions.UserError(
                "Отсутствует договор для заказчика, пожалуйста создайте его!"
            )
        if not len(
            self.mt_contractid.company_id.partner_id.child_ids.filtered(
                lambda r: not r.type != "director"
            )
        ):
            raise exceptions.UserError(
                "Не найден директор нашей кампании в договоре!Пожалуйста, создайте директора нашей кампании или добавьте нашу кампанию!"
            )
        if not self.mt_contractid.company_id.partner_id.child_ids.filtered(
            lambda r: not r.type != "director"
        )[0].name:
            raise exceptions.UserError(
                "Имя директора нашей кампании в договоре пустое!Пожалуйста, введите имя директора в формате Ф И О!"
            )

        if not len(
            self.mt_contractid.partner_id.child_ids.filtered(
                lambda r: not r.type != "director"
            )
        ):
            raise exceptions.UserError(
                "Не найден директор контрагента в договоре!Пожалуйста, создайте директора контрагента!"
            )
        if not self.mt_contractid.partner_id.child_ids.filtered(
            lambda r: not r.type != "director"
        )[0].name:
            raise exceptions.UserError(
                "Имя директора контрагента пустое!Пожалуйста, введите имя директора контрагента в формате Ф И О!"
            )

        # if not self.mt_contractid.partner_id.okpo:
        #     raise exceptions.UserError('Не присвоен ОКПО')
        partner_bank = (
            self.mt_contractid.partner_id.bank_ids
            and self.mt_contractid.partner_id.bank_ids.filtered(
                lambda r: r.company_id == self.mt_contractid.company_id
            )
        )
        if not partner_bank:
            partner_bank = (
                self.mt_contractid.partner_id.bank_ids
                and self.mt_contractid.partner_id.bank_ids[-1]
            )
        company_bank = (
            self.mt_contractid.company_id.partner_id.bank_ids
            and self.mt_contractid.company_id.partner_id.bank_ids[-1]
        )
        return {
            "phone": self.partner_id.phone,
            "contract_name": self.mt_contractid.name,
            "our_dir": self.mt_contractid.name_dirprint,
            "customer_dir": self.mt_contractid.name_print,
            "contract_date_start": fields.Date.from_string(
                self.mt_contractid.date_start
            ).strftime("%d.%m.%Y"),
            "contract_date_end": fields.Date.from_string(
                self.mt_contractid.date_end
            ).strftime("%d.%m.%Y"),
            "order_line": [line.read()[0] for line in self.order_line],
            "amount_total": self.amount_total,
            "amount_tax": self.amount_tax,
            "order_date": fields.Date.from_string(self.date_order).strftime(
                "%d.%m.%Y"
            ),
            # CUSTOMER
            "partner_name": self.mt_contractid.partner_id.name,
            "partner_inn": self.mt_contractid.partner_id.inn,
            "partner_kpp": self.mt_contractid.partner_id.kpp,
            "partner_ogrn": self.mt_contractid.partner_id.ogrn,
            "partner_okpo": self.mt_contractid.partner_id.okpo,
            "partner_address": self.format_partner(
                self.mt_contractid.partner_id
            ),
            "p_bank_bic": partner_bank.bank_bic or "",
            "p_acc_number": partner_bank.acc_number or "",
            "p_bank_name": partner_bank.bank_name or "",
            "p_cor_number": partner_bank.bank_id.correspondent_account or "",
            "p_mobile": self.mt_contractid.partner_id.mobile or "",
            "p_phone": self.mt_contractid.partner_id.phone or "",
            "p_email": self.mt_contractid.partner_id.email or "",
            "p_print_dir": len(
                self.mt_contractid.partner_id.child_ids.filtered(
                    lambda r: not r.type != "director"
                )
            )
            and self.mt_contractid.partner_id.child_ids.filtered(
                lambda r: not r.type != "director"
            )[0].name,
            # COMPANY
            "contract_company_name": self.mt_contractid.company_id.partner_id.name,
            "c_name": self.mt_contractid.company_id.partner_id.name,
            "c_inn": self.mt_contractid.company_id.partner_id.inn,
            "c_kpp": self.mt_contractid.company_id.partner_id.kpp or "",
            # не печатаем False для ИП, так как у ИП нет ОГРН и ОКПО
            "c_ogrn": self.mt_contractid.company_id.partner_id.ogrn
            if self.mt_contractid.company_id.partner_id.ogrn
            else "",
            "c_okpo": self.mt_contractid.company_id.partner_id.okpo
            if self.mt_contractid.company_id.partner_id.okpo
            else "",
            "c_address": self.format_partner(
                self.mt_contractid.company_id.partner_id
            ),
            "c_bank_bic": company_bank.bank_bic or "",
            "c_acc_number": company_bank.acc_number or "",
            "c_bank_name": company_bank.bank_name or "",
            "c_cor_number": company_bank.bank_id.correspondent_account or "",
            "c_mobile": self.mt_contractid.company_id.partner_id.mobile or "",
            "c_phone": self.mt_contractid.company_id.partner_id.phone or "",
            "c_email": self.mt_contractid.company_id.partner_id.email or "",
            "c_print_dir": len(
                self.mt_contractid.company_id.partner_id.child_ids.filtered(
                    lambda r: not r.type != "director"
                )
            )
            and self.mt_contractid.company_id.partner_id.child_ids.filtered(
                lambda r: not r.type != "director"
            )[0].name,
            # IMAGES
            # 1.jpg, 2.jpg, 3.jpg, 4.jpg, 5.jpg, 6.jpg, 7.jpg. 1,2.jpg = печать. 3,4,5,6,7.jpg = подпись. Печать и подпись берутся динамически из полей.
            "images": [
                self.mt_contractid.company_id.stamp,
                self.mt_contractid.company_id.stamp,
                self.mt_contractid.company_id.chief_id.facsimile,
                self.mt_contractid.company_id.chief_id.facsimile,
                self.mt_contractid.company_id.chief_id.facsimile,
                self.mt_contractid.company_id.chief_id.facsimile,
                self.mt_contractid.company_id.chief_id.facsimile,
            ]
            if self.mt_contractid.stamp
            else [False, False, False, False, False, False, False],
        }
