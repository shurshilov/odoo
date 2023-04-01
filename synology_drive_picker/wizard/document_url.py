# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (c) 2014 Serv. Tecnol. Avanzados (http://www.serviciosbaeza.com)
#                       Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>
#    Copyright (c) 2018 Shurshilov Artem (shurshilov.a@yandex.ru)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from odoo import fields, models, api
try:
    # Python 3
    from urllib.parse import urlparse
except:
    from urlparse import urlparse


class AddUrlWizard(models.TransientModel):
    _name = 'ir.attachment.add_url_gdrive'

    name = fields.Char('Name', required=True)
    url =  fields.Char('URL', required=True)

    @api.model
    def action_add_gdrive(self, docs):
        """Adds the Google Drive Document with an ir.attachment record."""
        context = self.env.context
        if not context.get('active_model'):
            return
        for doc in docs:
            url = urlparse(doc['url'])
            if not url.scheme:
                url = urlparse('%s%s' % ('http://', url))
            for active_id in context.get('active_ids', []):
                self.env['ir.attachment'].create({
                    'name': doc['name'],
                    'type': 'url',
                    'url': url.geturl(),
                    'res_id': active_id,
                    'res_model': context['active_model'],
                })
        return {'type': 'ir.actions.act_close_wizard_and_reload_attachments'}
