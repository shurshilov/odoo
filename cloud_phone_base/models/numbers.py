from odoo import fields, models


class Numbers(models.Model):
    _name = "cloud.phone.number"
    _description = "cloud.phone.number"

    tel = fields.Char(string="Tel number")
    name = fields.Char(string="Name")
    connector_id = fields.Many2one("cloud.phone.connector", string="Connector")
    connector_cloud_phone_vendor = fields.Selection(
        related="connector_id.cloud_phone_vendor", string="Connector name"
    )
    employee_id = fields.Many2one("hr.employee", string="Employee")
    # partner_id = fields.Many2one("res.partner", string="Partner")
    recording_in = fields.Boolean(string="recording_in", default=False)
    recording_out = fields.Boolean(string="recording_out", default=False)
    call_ids = fields.Many2many(
        string="Calls",
        comodel_name="cloud.phone.call",
        compute="_compute_call_ids",
    )
    lead_generation = fields.Selection(
        [
            ("self", "Create lead"),
            ("common", "Create common lead"),
            ("no", "No create lead"),
        ],
        string="Lead generation",
        default="self",
        help="Options for lead created by call",
    )

    def _compute_call_ids(self):
        for rec in self:
            rec.call_ids = self.env["cloud.phone.call"].search(
                [("number_id", "=", rec.id)]
            ) + self.env["cloud.phone.call"].search([("tel", "=", rec.tel)])

    def name_get(self):
        self = self.sudo()
        res = []
        for rec in self:
            name = "{}({} - {})".format(
                rec.tel,
                rec.employee_id.name or rec.name or "Не привязан",
                rec.connector_cloud_phone_vendor,
            )
            res.append((rec.id, name))
        return res
