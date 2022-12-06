# -*- coding: utf-8 -*-
from odoo import fields, models


class Events(models.Model):

    _name = "cloud.phone.event"
    _description = "cloud.phone.event"

    type = fields.Selection(
        [
            ("mango_event_call", "Звонок манго"),
            ("mango_event_summary", "Результат звонка манго"),
        ],
        default="mango_event_call",
        string="Тип события: ",
    )
    call_to = fields.Char(string="To")
    call_from = fields.Char(string="From")
    line_number = fields.Char(string="Line number")
    disconnect_reason = fields.Integer(string="Disconnect reason")
    params = fields.Char(string="Param event")
    body = fields.Char(string="Body event")
    connector_id = fields.Many2one("cloud.phone.connector", string="Connector")
