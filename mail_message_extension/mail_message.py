# -*- coding: utf-8 -*-
from openerp import models, fields, api
import logging
_logger = logging.getLogger(__name__)
class my_mypartner(models.Model):
    _name = 'my_mypartner'

    def default_author_id (self):
        context = self._context
        if context is None:
           context = {}
        _logger.info(self._context)
        return context.get('partner_id')

    author_id = fields.Many2one('res.partner', 'Author',default = default_author_id )
    name = fields.Char(related = 'author_id.name', string ='name')
    street = fields.Char(related = 'author_id.street', string ='name')

    def sync_visitors(self, cr, uid, partner_id, context=None):
        if not partner_id:
            return False
        return self.pool.get('my_mypartner').search(cr,uid,[('author_id.id','=',partner_id)])

class res_partner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    manager_id = fields.Many2one('my_mypartner', 'Manager')