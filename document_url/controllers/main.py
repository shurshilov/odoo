# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2012-today OpenERP SA (<http://www.openerp.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
##############################################################################
import logging
import werkzeug
import functools
import simplejson
import openerp
from openerp.addons.auth_signup.res_users import SignupError
from openerp.addons.web.controllers.main import ensure_db
from openerp import http
from openerp.http import request
from openerp.tools.translate import _
import logging
from openerp.http import request, serialize_exception as _serialize_exception
_logger = logging.getLogger(__name__)



try:
    # Python 3
    from urllib import parse as urlparse
except:
    from urlparse import urlparse

_logger = logging.getLogger(__name__)

def serialize_exception(f):
    @functools.wraps(f)
    def wrap(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception, e:
            _logger.exception("An exception occured during an http request")
            se = _serialize_exception(e)
            error = {
                'code': 200,
                'message': "Odoo Server Error",
                'data': se
            }
            return werkzeug.exceptions.InternalServerError(simplejson.dumps(error))
    return wrap

class Url(http.Controller):
    @http.route('/web/url/upload_attachment', type='http', auth="user")
    @serialize_exception
    def upload_attachment(self, url, urlname, model, id, callback):
        Model = request.session.model('ir.attachment')
        out = """<script language="javascript" type="text/javascript">
                    var win = window.top.window;
                    win.jQuery(win).trigger(%s, %s);
                </script>"""
        try:
            my_url = urlparse(url)
            if not my_url.scheme:
                my_url = urlparse('%s%s' % ('http://', url))
            attachment_id = Model.create({
                    'name': urlname,
                    'type': 'url',
                    'url': my_url.geturl(),
                    'filename': "link",
                    'res_id':  int(id),
                    'res_model': model,
            }, request.context)
            args = {
                'name': urlname,
                'url':  my_url.geturl(),
                'id':   attachment_id
            }
        except Exception:
            args = {'error': "Something horrible happened"}
            _logger.exception("Fail to upload attachment %s" % urlname)
        return out % (simplejson.dumps(callback), simplejson.dumps(args))
