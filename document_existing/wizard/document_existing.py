# -*- coding: utf-8 -*-

from openerp.osv import fields, orm

class AddExistingWizard(orm.TransientModel):
    _name = 'ir.attachment.add_existing_documents'

    _columns = {
        'documents_existing': fields.many2one('ir.attachment', 'name', required=True,domain="[('res_model', '!=' ,False)]" ), # ,domain=[]
    }

    def action_add_existing_document(self, cr, uid, ids, context=None):
        """Adds the URL with the given name as an ir.attachment record."""
        if context is None:
            context = {}
        if not context.get('active_model'):
            return
        attachment_obj = self.pool['ir.attachment']
        for form in self.browse(cr, uid, ids, context=context):
            exist_obj = form.documents_existing
            for active_id in context.get('active_ids', []):
                attachment = {
                    'name': exist_obj['name'],
                    'type': exist_obj['type'],
                    'url': exist_obj['url'],
                    'datas_fname': exist_obj['datas_fname'],
                    'store_fname': exist_obj['store_fname'],
                    'file_size': exist_obj['file_size'],
                    'user_id': uid,
                    'res_id': active_id,
                    'res_model': context['active_model'],
                }
                attachment_obj.create(cr, uid, attachment, context=context)
        return {'type': 'ir.actions.act_close_wizard_and_reload_view'}