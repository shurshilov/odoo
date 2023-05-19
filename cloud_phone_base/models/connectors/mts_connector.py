# -*- coding: utf-8 -*-
from odoo import fields, models


class Number(models.Model):

    _inherit = "cloud.phone.number"

    mts_tz = fields.Char(string="Timezone -1 to 9")


class Connector(models.Model):

    _inherit = "cloud.phone.connector"

    cloud_phone_vendor = fields.Selection(
        selection_add=[("mts", "MTS")], ondelete={"mts": "cascade"}
    )
