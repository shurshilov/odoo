# -*- coding: utf-8 -*-
# Copyright 2019 Shurshilov Artem
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models, _


class AccountInvoiceWizardCopy(models.TransientModel):
    _name = 'account.invoice.wizard.copy'

    new_date_invoice = fields.Date('New invoices date', required=True, default=fields.Date.today())
    new_date_due = fields.Date('New due Date', required=True, default=fields.Date.today())

    @api.multi
    def copy_invoice(self, records=False):
            if records:
                self._context['active_ids'] = records.ids
                return {
                    'name': _('Invoices copy wizard'),
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'account.invoice.wizard.copy',
                    'view_id': self.env.ref('account_invoices_copy.account_invoice_copy_view_copy_form').id,
                    'type': 'ir.actions.act_window',
                    'target': 'new',
                    'context': self._context,
                }

    @api.onchange('new_date_invoice')
    def onchange_new_date_invoice(self):
        self.new_date_due = self.new_date_invoice

    def create_invoices(self):
        for invoice_record in self.env['account.invoice'].browse(self._context.get('active_ids')):
            invoice_record.copy({
                 'date_invoice': self.new_date_invoice,
                 'date_due': self.new_date_due,
                 'user_id': self._context.get('uid'),
                 'reference': False,
                 'state': 'draft',
            })
