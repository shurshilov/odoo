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
    _name = 'ir.attachment.add_url'

    name = fields.Char('Name', required=True)
    url =  fields.Char('URL', required=True)

    @api.multi
    def action_add_url(self):
        """Adds the URL with the given name as an ir.attachment record."""
        if not self._context.get('active_model'):
            return
        attachment_obj = self.env['ir.attachment']
        for form in self:
            url = urlparse(form.url)
            if not url.scheme:
                url = urlparse('%s%s' % ('http://', form.url))
            attachment = {
                    'name': form.name,
                    'type': 'url',
                    #'url': form.url,
                    'url': url.geturl(),
                    'user_id': self._uid,
                    'res_id': self._context.get('active_record_id',False),
                    'res_model': self._context.get('active_model',False),
                }
            attachment_obj.create(attachment)
        return {'type': 'ir.actions.act_close_wizard_and_reload_view'}
