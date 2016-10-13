import base64
import psycopg2
import functools
import openerp
from openerp import SUPERUSER_ID
from openerp import http
from openerp.http import request
from openerp.addons.web.controllers.main import content_disposition
from openerp.addons.mail.controllers.main import MailController
from openerp.addons.web.controllers.main import Binary
import mimetypes
import logging
from openerp.http import request, serialize_exception as _serialize_exception
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

class MyMailController(MailController):
    _cp_path = '/mail'

    @http.route('/mail/download_attachment', type='http', auth='user')
    def download_attachment(self, model, id, method, attachment_id, **kw):
        result = super(MyMailController, self).download_attachment(model, id, method, attachment_id, **kw)
        result.headers['Content-Disposition'] = result.headers['Content-Disposition'].replace('attachment', 'inline')
        return result

class MyBinary(Binary):  
    @http.route('/web/binary/saveas', type='http', auth="public")
    def saveas(self, model, field, id=None, filename_field=None, **kw):
        Model = request.registry[model]
        cr, uid, context = request.cr, request.uid, request.context
        fields = [field]
        if filename_field:
            fields.append(filename_field)
        if id:
            res = Model.read(cr, uid, [int(id)], fields, context)[0]
        else:
            res = Model.default_get(cr, uid, fields, context)
        filecontent = base64.b64decode(res.get(field) or '')
        
        if not filecontent:
            return request.not_found()
        else:
            content_type = ""
            filename = '%s_%s' % (model.replace('.', '_'), id)            
            if filename_field:
                filename = res.get(filename_field, '') or filename
                content_type = mimetypes.guess_type(filename)
            return request.make_response(filecontent,
                headers=[('Content-Type',  content_type[0] or 'application/octet-stream'),
                 ('Content-Disposition', content_disposition(filename).replace('attachment', 'inline'))])