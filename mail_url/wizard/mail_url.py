# -*- coding: utf-8 -*-
from openerp import models, fields, api, SUPERUSER_ID
import openerp

class mail_message(models.Model):
    _name = 'mail.message'
    _inherit = 'mail.message'
    _description = 'Message'
    def _message_read_dict_postprocess(self, cr, uid, messages, message_tree, context=None):
        """ Post-processing on values given by message_read. This method will
            handle partners in batch to avoid doing numerous queries.

            :param list messages: list of message, as get_dict result
            :param dict message_tree: {[msg.id]: msg browse record}
        """
        res_partner_obj = self.pool.get('res.partner')
        ir_attachment_obj = self.pool.get('ir.attachment')
        pid = self.pool['res.users'].browse(cr, SUPERUSER_ID, uid, context=context).partner_id.id

        # 1. Aggregate partners (author_id and partner_ids) and attachments
        partner_ids = set()
        attachment_ids = set()
        for key, message in message_tree.iteritems():
            if message.author_id:
                partner_ids |= set([message.author_id.id])
            if message.subtype_id and message.notified_partner_ids:  # take notified people of message with a subtype
                partner_ids |= set([partner.id for partner in message.notified_partner_ids])
            elif not message.subtype_id and message.partner_ids:  # take specified people of message without a subtype (log)
                partner_ids |= set([partner.id for partner in message.partner_ids])
            if message.attachment_ids:
                attachment_ids |= set([attachment.id for attachment in message.attachment_ids])
        # Read partners as SUPERUSER -> display the names like classic m2o even if no access
        partners = res_partner_obj.name_get(cr, SUPERUSER_ID, list(partner_ids), context=context)
        partner_tree = dict((partner[0], partner) for partner in partners)

        # 2. Attachments as SUPERUSER, because could receive msg and attachments for doc uid cannot see
        #MY CODE: APPEND type and url to return read message
        attachments = ir_attachment_obj.read(cr, SUPERUSER_ID, list(attachment_ids), ['id', 'datas_fname', 'name', 'type', 'url', 'file_type_icon'], context=context)
        attachments_tree = dict((attachment['id'], {
            'id': attachment['id'],
            'filename': attachment['datas_fname'],
            'name': attachment['name'],
            'type': attachment['type'],
            'url': attachment['url'],
            'file_type_icon': attachment['file_type_icon'],
        }) for attachment in attachments)

        # 3. Update message dictionaries
        for message_dict in messages:
            message_id = message_dict.get('id')
            message = message_tree[message_id]
            if message.author_id:
                author = partner_tree[message.author_id.id]
            else:
                author = (0, message.email_from)
            partner_ids = []
            if message.subtype_id:
                partner_ids = [partner_tree[partner.id] for partner in message.notified_partner_ids
                                if partner.id in partner_tree]
            else:
                partner_ids = [partner_tree[partner.id] for partner in message.partner_ids
                                if partner.id in partner_tree]
            attachment_ids = []
            for attachment in message.attachment_ids:
                if attachment.id in attachments_tree:
                    attachment_ids.append(attachments_tree[attachment.id])
            message_dict.update({
                'is_author': pid == author[0],
                'author_id': author,
                'partner_ids': partner_ids,
                'attachment_ids': attachment_ids,
                'user_pid': pid
                })
        return True