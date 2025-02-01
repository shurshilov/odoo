from odoo import models, fields, api
import requests

try:
    # Python 3
    from urllib.parse import urlparse
    from urllib.parse import urlencode
    from urllib.parse import parse_qsl
    from urllib.parse import urlunparse
except:
    from urlparse import urlparse
    from urlparse import parse_qsl
    from urlparse import urlunparse
    from urllib import urlencode
from datetime import datetime

# import logging
# _logger = logging.getLogger(__name__)


class ResUsers(models.Model):
    _inherit = "res.users"

    oauth_uid_vk = fields.Char(
        string="User ID", help="Oauth Provider user_id", readonly=True, copy=False
    )
    oauth_access_token_vk = fields.Char(string="Access token", readonly=True, copy=False)
    code = fields.Char(string="Code", readonly=True, copy=False)
    expires_in = fields.Char(string="Expires in", readonly=True, copy=False)
    user_email_vk = fields.Char(string="User email", readonly=True, copy=False)
    date_bithday = fields.Date(string="Bithday", readonly=True, copy=False)


class open_vk(models.Model):
    _name = "open_vk.open_vk"

    client_id = fields.Char(string="Client ID", required=True)
    client_secret = fields.Char(string="Client secret", required=True)
    auth_endpoint = fields.Char(
        string="Authentication URL", required=True, default="https://oauth.vk.com/authorize"
    )

    validation_endpoint = fields.Char(
        string="Validation URL", required=True, default="https://oauth.vk.com/access_token"
    )

    redirect_uri = fields.Char(
        string="Redirect URI", required=True, default="http://127.0.0.1:8069/open_vk/open_vk/auth"
    )

    display = fields.Selection(
        [
            ("page", "форма авторизации в отдельном окне"),
            ("popup", "всплывающее окно"),
            ("mobile", "авторизация для мобильных устройств"),
        ],
        default="popup",
    )

    scope = fields.Char(string="Scope", default="email")
    response_type = fields.Char(string="Response type", default="code")
    version = fields.Char(string="Version", required=True, default="5.80")
    # code = fields.Char(string='Code', readonly=True)
    link = fields.Char(string="Link to login", readonly=True)
    log = fields.Text(default="История запросов")
    provider_vk_id = fields.Many2one("auth.oauth.provider", "Provider", readonly=True)
    sequence = fields.Integer("sequence", default=10)

    @api.model
    def create(self, vals):
        params = {
            "client_id": vals.get("client_id", self.client_id),
            "redirect_uri": vals.get("redirect_uri", self.redirect_uri),
            "display": vals.get("display", self.display),
            "response_type": vals.get("response_type", self.response_type),
            "v": vals.get("version", self.version),
            "state": vals.get("id", self.id),
            "scope": vals.get("scope", self.scope),
        }
        try:  # Python 2
            url_parts = list(urlparse(vals.get("auth_endpoint", self.auth_endpoint)))
        except:
            url_parts = list(urlparse(vals.get("auth_endpoint", self.auth_endpoint)))
        query = dict(parse_qsl(url_parts[4]))
        query.update(params)
        url_parts[4] = urlencode(query)
        vals["link"] = urlunparse(url_parts) + "#"

        provider_vk_id = self.env["auth.oauth.provider"].search(
            [("name", "=", "Vkontakte")], limit=1
        )
        if not provider_vk_id:
            provider_vk_id = self.env["auth.oauth.provider"].create(
                {
                    "name": "Vkontakte",
                    "auth_endpoint": vals.get("link", self.link),
                    "validation_endpoint": "not use",
                    "body": "Log in with Vkontakte",
                    "enabled": True,
                }
            )
            vals["provider_vk_id"] = provider_vk_id.id
        else:
            provider_vk_id.auth_endpoint = vals.get("link", self.link)
            vals["provider_vk_id"] = provider_vk_id.id
        res = super().create(vals)
        res.write({"state": res.id})
        return res

    @api.multi
    def write(self, vals):
        params = {
            "client_id": vals.get("client_id", self.client_id),
            "redirect_uri": vals.get("redirect_uri", self.redirect_uri),
            "display": vals.get("display", self.display),
            "response_type": vals.get("response_type", self.response_type),
            "v": vals.get("version", self.version),
            "state": vals.get("id", self.id),
            "scope": vals.get("scope", self.scope),
        }
        url_parts = list(urlparse(vals.get("auth_endpoint", self.auth_endpoint)))
        query = dict(parse_qsl(url_parts[4]))
        query.update(params)
        url_parts[4] = urlencode(query)
        vals["link"] = urlunparse(url_parts) + "#"

        provider_vk_id = self.env["auth.oauth.provider"].search(
            [("name", "=", "Vkontakte")], limit=1
        )
        if not provider_vk_id:
            provider_vk_id = self.env["auth.oauth.provider"].create(
                {
                    "name": "Vkontakte",
                    "auth_endpoint": vals.get("link", self.link),
                    "validation_endpoint": "not use",
                    "body": "Log in with Vkontakte",
                    "enabled": True,
                }
            )
            vals["provider_vk_id"] = provider_vk_id.id
        else:
            provider_vk_id.auth_endpoint = vals.get("link", self.link)
            vals["provider_vk_id"] = provider_vk_id.id
        res = super().write(vals)
        return res

    @api.multi
    def get_access_token(self, code):
        for rec in self:
            params = {
                "client_id": rec.client_id,
                "redirect_uri": rec.redirect_uri,
                "client_secret": rec.client_secret,
                "code": code,
                "state": rec.id,
            }
            response = requests.get(rec.validation_endpoint, params=params).json()
            rec.log += "\n" + datetime.now().strftime("%Y-%m-%d/%H-%m") + str(response)
            return response

    @api.multi
    def login(self, code):
        for rec in self:
            r = self.get_access_token(code)
            if r.get("access_token", False):
                profile = self.get_profile_info(r)
                user_vk = self.env["res.users"].search(
                    [
                        "|",
                        ("login", "=", r.get("email", False)),
                        ("email", "=", r.get("email", False)),
                    ],
                    limit=1,
                )
                user_data = {
                    "name": profile.get("first_name", False)
                    + " "
                    + profile.get("last_name", False),
                    "login": r.get("email", r.get("access_token", False)),
                    "email": r.get("email", "notfound@gmail.com"),
                    "oauth_provider_id": rec.provider_vk_id.id,
                    "oauth_uid_vk": r.get("user_id", False),
                    "oauth_access_token_vk": r.get("access_token", False),
                    "code": code,
                    "expires_in": r.get("expires_in", False),
                    "user_email_vk": r.get("email", False),
                    "date_bithday": datetime.strptime(
                        profile.get("bdate", "01.01.2020"), "%d.%m.%Y"
                    ),
                }
                login = r.get("email", False)
                if user_vk:
                    user_vk.write(user_data)
                    user_vk.password = r.get("access_token", False)
                    login = user_vk.login
                else:
                    user_vk = self.env["res.users"].create(user_data)
                    user_vk.password = r.get("access_token", False)
                self._cr.commit()
                retid = user_vk.id

                params = {
                    "password": r.get("access_token", False),
                    "login": login,
                    "user_vk": retid,
                }
                return ["signin", params]

    @api.multi
    def get_profile_info(self, response):
        for rec in self:
            params = {
                "user_ids": response["user_id"],
                "access_token": response["access_token"],
                "v": rec.version,
                "fields": "bdate, city, country, last_seen",
            }
            response = requests.get("https://api.vk.com/method/users.get", params=params).json()
            r = response.get("response")[0]
            return r
