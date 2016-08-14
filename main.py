import base64
import psycopg2

import openerp
from openerp import SUPERUSER_ID
from openerp import http
from openerp.http import request
from openerp.addons.web.controllers.main import content_disposition
from openerp.addons.mail.controllers.main import MailController
import mimetypes


class MyMailController(MailController):
    _cp_path = '/mail'

    @http.route('/mail/download_attachment', type='http', auth='user')
    def download_attachment(self, model, id, method, attachment_id, **kw):
        # FIXME use /web/binary/saveas directly
        Model = request.registry.get(model)
        res = getattr(Model, method)(request.cr, request.uid, int(id), int(attachment_id))
        if res:
            filecontent = base64.b64decode(res.get('base64'))
            filename = res.get('filename')
            content_type = mimetypes.guess_type(filename)
            if filecontent and filename:
                return request.make_response(
                    filecontent,
                    headers=[('Content-Type', content_type[0] or 'application/octet-stream'),
                             ('Content-Disposition', content_disposition(filename).replace('attachment', 'inline'))])
        return request.not_found()