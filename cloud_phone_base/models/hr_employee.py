from odoo import models, fields

class HrEmployee(models.Model):
    _inherit = "hr.employee"

    call_ids = fields.Many2many(string="Calls",
        comodel_name="cloud.phone.call",
        compute="_compute_call_ids")

    def _compute_call_ids(self):
        for rec in self:
            number_id = self.env["cloud.phone.number"].search([('employee_id', '=', rec.id)])
            if number_id:
                rec.call_ids = (self.env["cloud.phone.call"].search([('number_id', '=', number_id.id)]) +
                self.env["cloud.phone.call"].search([('tel', '=', number_id.tel)]))
            else:
                rec.call_ids = False