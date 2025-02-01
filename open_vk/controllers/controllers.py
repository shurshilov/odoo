from odoo import http
from odoo import SUPERUSER_ID
from werkzeug.exceptions import BadRequest
from odoo.http import request
from odoo.addons.web.controllers.main import ensure_db


# import logging
# _logger = logging.getLogger(__name__)
class OpenVk(http.Controller):
    @http.route("/open_vk/open_vk/auth/", auth="public")
    def list(self, **kw):
        env = http.request.env(user=SUPERUSER_ID)
        if kw.get("error", False):
            return http.request.render(
                "open_vk.error",
                {
                    "error": kw.get("error", False),
                },
            )

        if kw.get("code", False) and kw.get("state", False):
            rec = env["open_vk.open_vk"].search([("id", "=", kw.get("state", False))])
            # rec.write({'code': kw.get("code", False)})
            ret = rec.login(kw.get("code", False))
            if ret[0] == "signup":
                # signup_prepare
                return http.local_redirect("/web/signup", query=ret[1], keep_hash=True)

            if ret[0] == "signin":
                ensure_db()
                request.params["login_success"] = False
                if not request.uid:
                    request.uid = SUPERUSER_ID
                uid = request.session.authenticate(
                    request.session.db, ret[1]["login"], ret[1]["password"], ret[1]["user_vk"]
                )
                if uid is not False:
                    request.params["login_success"] = True
                    return http.redirect_with_hash("/web")
            return http.redirect_with_hash("/web")
        return BadRequest()
