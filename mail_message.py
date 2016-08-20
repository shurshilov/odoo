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