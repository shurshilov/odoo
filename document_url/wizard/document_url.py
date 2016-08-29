# -*- coding: utf-8 -*-
from openerp import models, fields, api
import openerp
'''
class mail_message(models.Model):

    _description = 'Message'
    _inherit = 'mail.message'
    def _update_email_from(self, cr, uid, message_id, context=None):
        email_from = 'test@example.dom'
        self.write(cr, uid, [message_id], {'email_from': email_from}, context=context)

    def create(self, cr, uid, vals, context=None):
        context = dict(context or {})
        message_id = super(MailMessage, self).create(cr, uid, vals, context=context)
        self._update_email_from(cr, uid, message_id, context=context)
        return message_id
    def download_attachment(self, cr, uid, id_message, attachment_id, context=None):
        """ Return the content of linked attachments. """
        # this will fail if you cannot read the message
        message_values = self.read(cr, uid, [id_message], ['attachment_ids'], context=context)[0]
        if attachment_id in message_values['attachment_ids']:
            attachment = self.pool.get('ir.attachment').browse(cr, SUPERUSER_ID, attachment_id, context=context)
            if attachment.datas and attachment.datas_fname:
                return {
                    'base64': attachment.datas,
                    'filename': attachment.datas_fname,
                }
        return {'filename': "url"}
'''