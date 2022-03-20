# -*- coding: utf-8 -*-

from odoo import http
from odoo.addons.web.controllers.main import Home
from odoo.addons.website.controllers.main import Website
from odoo.http import request


class Frontend(Website):
    @http.route('/', type='http', auth="public", website=True)
    def index(self, **kw):
        yandex_metrica = request.env['ir.config_parameter'].sudo().get_param('yandex_metric')
        if yandex_metrica:
            request.params['yandex_metrica'] = yandex_metrica
        return super(Frontend, self).index(**kw)

class Backend(Home):

    # ideally, this route should be `auth="user"` but that don't work in non-monodb mode.
    @http.route('/web', type='http', auth="none")
    def web_client(self, s_action=None, **kw):
        yandex_metrica = request.env['ir.config_parameter'].sudo().get_param('yandex_metric')
        if yandex_metrica:
            request.params['yandex_metrica'] = yandex_metrica
        return super(Backend, self).web_client(s_action=s_action, **kw)

    @http.route('/web/login', type='http', auth="public")
    def web_login(self, redirect=None, **kw):
        yandex_metrica = request.env['ir.config_parameter'].sudo().get_param('yandex_metric')
        if yandex_metrica:
            request.params['yandex_metrica'] = yandex_metrica
        return super(Backend, self).web_login(redirect=redirect, **kw)
