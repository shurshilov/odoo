from odoo import fields, models


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    call_ids = fields.Many2many(
        string="Calls",
        comodel_name="cloud.phone.call",
        compute="_compute_call_ids",
    )

    def _compute_call_ids(self):
        for rec in self:
            number_ids = self.env["cloud.phone.number"].search(
                [("employee_id", "=", rec.id)]
            )
            if number_ids:
                rec.call_ids = self.env["cloud.phone.call"].search(
                    [("number_id", "in", number_ids.ids)]
                ) + self.env["cloud.phone.call"].search(
                    [("tel", "in", [number.tel for number in number_ids])]
                )
            else:
                rec.call_ids = False
