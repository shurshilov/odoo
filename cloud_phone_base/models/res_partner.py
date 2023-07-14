from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    call_ids = fields.Many2many(
        string="Calls",
        comodel_name="cloud.phone.call",
        compute="_compute_call_ids",
    )

    def _compute_call_ids(self):
        """
        Searches for all calls in which the phone number matches
        the mobile/work number and also searches without
        the first character (country code)
        """
        for rec in self:
            rec.call_ids = False
            if rec.mobile:
                mobile = "".join(i for i in rec.mobile if i.isdigit())
                if mobile:
                    rec.call_ids += self.env["cloud.phone.call"].search(
                        [
                            "|",
                            ("number_id.tel", "=", "7" + mobile[1:]),
                            "|",
                            ("number_id.tel", "=", mobile[1:]),
                            ("number_id.tel", "=", mobile),
                        ]
                    )
                    rec.call_ids += self.env["cloud.phone.call"].search(
                        [
                            "|",
                            ("tel", "=", "7" + mobile[1:]),
                            "|",
                            ("tel", "=", mobile[1:]),
                            ("tel", "=", mobile),
                        ]
                    )
            if rec.phone:
                phone = "".join(i for i in rec.phone if i.isdigit())
                if phone:
                    rec.call_ids += self.env["cloud.phone.call"].search(
                        [
                            "|",
                            ("number_id.tel", "=", "7" + phone[1:]),
                            "|",
                            ("number_id.tel", "=", phone[1:]),
                            ("number_id.tel", "=", phone),
                        ]
                    )
                    rec.call_ids += self.env["cloud.phone.call"].search(
                        [
                            "|",
                            ("tel", "=", "7" + phone[1:]),
                            "|",
                            ("tel", "=", phone[1:]),
                            ("tel", "=", phone),
                        ]
                    )
