from odoo import exceptions, models


class mta_partner_contract(models.Model):
    _inherit = "partner.contract.customer"

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

    def get_report_context_supplier(self):
        """
        контекст для договора поставщика МЫ-заказчик ОН-исполнитель
        """
        try:
            self = self.sudo()
            if not len(
                self.company_id.partner_id.child_ids.filtered(
                    lambda r: not r.type != "director"
                )
            ):
                raise exceptions.UserError(
                    "Не найден директор нашей кампании в договоре!Пожалуйста, создайте директора нашей кампании или добавьте нашу кампанию!"
                )
            if not self.company_id.partner_id.child_ids.filtered(
                lambda r: not r.type != "director"
            )[0].name:
                raise exceptions.UserError(
                    "Имя директора нашей кампании в договоре пустое!Пожалуйста, введите имя директора в формате Ф И О!"
                )

            if not len(
                self.partner_id.child_ids.filtered(
                    lambda r: not r.type != "director"
                )
            ):
                raise exceptions.UserError(
                    "Не найден директор контрагента в договоре!Пожалуйста, создайте директора контрагента!"
                )
            if not self.partner_id.child_ids.filtered(
                lambda r: not r.type != "director"
            )[0].name:
                raise exceptions.UserError(
                    "Имя директора контрагента пустое!Пожалуйста, введите имя директора контрагента в формате Ф И О!"
                )

            partner_bank = (
                self.partner_id.bank_ids
                and self.partner_id.bank_ids.filtered(
                    lambda r: r.company_id == self.company_id
                )
            )
            if not partner_bank:
                partner_bank = (
                    self.partner_id.bank_ids and self.partner_id.bank_ids[-1]
                )
            company_bank = (
                self.company_id.partner_id.bank_ids
                and self.company_id.partner_id.bank_ids[-1]
            )
            return {
                # COMMON
                "contract_date_start": self.date_start.strftime("%d.%m.%Y"),
                "contract_date_end": self.date_end.strftime("%d.%m.%Y"),
                "our_dir": self.name_dirprint,
                "customer_dir": self.name_print,
                "order_line": [line.read()[0] for line in self.lines],
                # CUSTOMER
                "partner_name": self.partner_id.name,
                "partner_inn": self.partner_id.inn,
                "partner_kpp": self.partner_id.kpp,
                "partner_ogrn": self.partner_id.ogrn,
                "partner_okpo": self.partner_id.okpo,
                "partner_address": self.format_partner(self.partner_id),
                "p_bank_bic": partner_bank.bank_bic or "",
                "p_acc_number": partner_bank.acc_number or "",
                "p_bank_name": partner_bank.bank_name or "",
                "p_cor_number": partner_bank.bank_id.correspondent_account
                or "",
                "p_mobile": self.partner_id.mobile or "",
                "p_phone": self.partner_id.phone or "",
                "p_email": self.partner_id.email or "",
                "p_print_dir": len(
                    self.partner_id.child_ids.filtered(
                        lambda r: not r.type != "director"
                    )
                )
                and self.partner_id.child_ids.filtered(
                    lambda r: not r.type != "director"
                )[0].name,
                # COMPANY
                "contract_company_name": self.company_id.partner_id.name,
                "contract_name": self.name,
                "c_inn": self.company_id.partner_id.inn,
                "c_kpp": self.company_id.partner_id.kpp or "",
                "c_ogrn": self.company_id.partner_id.ogrn
                if self.company_id.partner_id.ogrn
                else "",
                "c_okpo": self.company_id.partner_id.okpo
                if self.company_id.partner_id.okpo
                else "",
                "c_address": self.format_partner(self.company_id.partner_id),
                "c_bank_bic": company_bank.bank_bic or "",
                "c_acc_number": company_bank.acc_number or "",
                "c_bank_name": company_bank.bank_name or "",
                "c_cor_number": company_bank.bank_id.correspondent_account
                or "",
                "c_mobile": self.company_id.partner_id.mobile or "",
                "c_phone": self.company_id.partner_id.phone or "",
                "c_email": self.company_id.partner_id.email or "",
                "c_print_dir": len(
                    self.company_id.partner_id.child_ids.filtered(
                        lambda r: not r.type != "director"
                    )
                )
                and self.company_id.partner_id.child_ids.filtered(
                    lambda r: not r.type != "director"
                )[0].name,
                # IMAGES
                # 1.jpg, 2.jpg, 3.jpg, 4.jpg, 5.jpg, 6.jpg, 7.jpg. 1,2.jpg = печать. 3,4,5,6,7.jpg = подпись. Печать и подпись берутся динамически из полей.
                "images": [
                    self.company_id.stamp,
                    self.company_id.stamp,
                    self.company_id.chief_id.facsimile,
                    self.company_id.chief_id.facsimile,
                    self.company_id.chief_id.facsimile,
                    self.company_id.chief_id.facsimile,
                    self.company_id.chief_id.facsimile,
                ]
                if self.stamp
                else [False, False, False, False, False, False, False],
            }
        except Exception as e:
            raise exceptions.UserError(str(e))
