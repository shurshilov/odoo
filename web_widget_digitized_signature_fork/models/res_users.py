# Copyright (C) 2021-2024 Artem Shurshilov <shurshilov.a@yandex.ru>
# License OPL-1.0

from odoo import fields, models


class ResUsers(models.Model):
    _name = "res.users"
    _inherit = ["res.users", "mail.thread"]

    digital_signature = fields.Binary(
        string="Digital Signature", attachment=True
    )

    # @api.model_create_multi
    # def create(self, vals):
    #     res = super().create(vals)
    #     res._track_signature(vals, "digital_signature")
    #     return res

    # # @api.multi
    # def write(self, vals):
    #     self._track_signature(vals, "digital_signature")
    #     return super().write(vals)
