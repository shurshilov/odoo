# -*- coding: utf-8 -*-
from openerp import _, api, fields, models, SUPERUSER_ID
class MailComposer(models.TransientModel):
    _name = 'mail.compose.message'
    _inherit = 'mail.compose.message'

    def default_body(self):
        context = self._context
        if context is None:
            context = {}
        return context.get('body')
    def default_subject(self):
        context = self._context
        if context is None:
            context = {}
        return context.get('subject')
    @api.model
    def get_record_data(self, values):
        result = super(MailComposer, self).get_record_data(values)
        result['body'] = self.default_body()
        result['subject'] = self.default_subject()
        return result