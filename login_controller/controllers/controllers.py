# -*- coding: utf-8 -*-
# Copyright 2021 Artem Shurshilov

from odoo import http
from odoo.http import request
import werkzeug
from werkzeug import url_encode
from odoo import _, SUPERUSER_ID
from odoo.tools import config


class Login(http.Controller):
    @http.route('/login_employee', type='http', auth='none', methods=['GET'], csrf=False)
    def login_action(self, login, password, action='contacts.action_contacts', db=None, force='', mod_file=None, **kw):
        if db and db != request.db:
            raise Exception(_("Could not select database '%s'") % db)
        uid = request.session.authenticate(request.db, login, password)
        url = '/web#%s' % url_encode({'action': action})
        return werkzeug.utils.redirect(url)
