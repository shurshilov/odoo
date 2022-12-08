# -*- coding: utf-8 -*-
from odoo import fields, models


class Calls(models.Model):

    _name = "cloud.phone.call"
    _description = "cloud.phone.call"
    _order = "time desc"

    tel = fields.Char(string="Tel number")
    compute_tel = fields.Char(string="Tel number", compute="_compute_tel")
    time = fields.Datetime(string="Time")
    external_id = fields.Char(string="External id")
    number_id = fields.Many2one("cloud.phone.number", string="Number")
    connector_id = fields.Many2one("cloud.phone.connector", string="Connector")
    type = fields.Selection(
        [("incoming", "Incoming"), ("outgoing", "Outgoing")],
        required=True,
        default="incoming",
    )
    ir_attachment_id = fields.Many2one("ir.attachment", string="Audio/video record")
    rec_duration = fields.Char(string="RecDuration")
    call_duration = fields.Char(string="CallDuration")
    filename = fields.Char(string="FileName")

    def _compute_tel(self):
        self = self.sudo()
        for rec in self:
            number_id = self.env["cloud.phone.number"].search([("tel", "=", rec.tel)])
            employee = ""
            if number_id and number_id.employee_id:
                employee = "(" + number_id.employee_id.name + ")"
            rec.compute_tel = "{}{}".format(rec.tel, employee)

    def name_get(self):
        self = self.sudo()
        res = []
        for rec in self:
            number_name = "{}({} - {})".format(
                rec.number_id.tel,
                rec.number_id.employee_id.name or rec.number_id.name or "Не привязан",
                rec.number_id.connector_cloud_phone_vendor,
            )
            if rec.type == "incoming":
                name = "{} - {}".format(rec.tel, number_name)
            else:
                name = "{} - {}".format(number_name, rec.tel)
            res.append((rec.id, name))
        return res
