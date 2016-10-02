# -*- coding: utf-8 -*-
import logging
import werkzeug
import functools
import simplejson
import openerp
import base64
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
    def upload_attachment_url(self, url, urlname, model, id, callback):
        Model = request.session.model('ir.attachment')
        out = """<script language="javascript" type="text/javascript">
                    var win = window.top.window;
                    win.jQuery(win).trigger(%s, %s);
                </script>"""
        try:
            #url = "http://"+url;
            my_url = urlparse(url)
            if not my_url.scheme:
                my_url = urlparse('%s%s' % ('http://', url))
            attachment_id = Model.create({
                    'name': urlname,
                    'type': 'url',
                    'url': my_url.geturl(),
                    'res_id':  int(id),
                    'res_model': model,
            }, request.context)
            args = {
                'name': urlname,
                'url':  my_url.geturl(),
                'id':   attachment_id,
                'type':   'url',
            }
        except Exception:
            args = {'error': "Something horrible happened"}
            _logger.exception("Fail to upload attachment %s" % urlname)
        return out % (simplejson.dumps(callback), simplejson.dumps(args))

    @http.route('/web/mybinary/upload_attachment', type='http', auth="user")
    @serialize_exception
    def upload_attachment_file(self, callback, model, id, ufile, filename1):
        Model = request.session.model('ir.attachment')
        out = """<script language="javascript" type="text/javascript">
                    var win = window.top.window;
                    win.jQuery(win).trigger(%s, %s);
                </script>"""
        try:
            if not filename1:
                filename = ufile.filename
            else:
                filename = filename1
            attachment_id = Model.create({
                'name': filename,
                'datas': base64.encodestring(ufile.read()),
                'datas_fname': ufile.filename,
                'res_model': model,
                'res_id': int(id)
            }, request.context)
            args = {
                'filename': ufile.filename,
                'id':  attachment_id,
                'name': filename,
            }
        except Exception:
            args = {'error': "Something horrible happened"}
            _logger.exception("Fail to upload attachment %s" % ufile.filename)
        return out % (simplejson.dumps(callback), simplejson.dumps(args))

