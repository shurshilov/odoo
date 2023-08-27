from odoo import api, fields, models


class mta_saleorder(models.Model):
    _inherit = "sale.order"
    mt_contractid = fields.Many2one(
        "partner.contract.customer", string="Договор"
    )

    # аналог one2one возможно лучше заменить на compute или inherits
    @api.constrains("mt_contractid")
    def save_cont_id(self):
        if self.mt_contractid:
            contract = self.env["partner.contract.customer"].browse(
                self.mt_contractid.id
            )
            contract.saleorder_id = self.id

    def print_contract(self):
        return (
            self.env["ir.actions.report"]
            .sudo()
            ._get_report_from_name(
                "mcontract.report_custcontractp_template_docx1"
            )
            .sudo()
            .report_action(self)
        )
