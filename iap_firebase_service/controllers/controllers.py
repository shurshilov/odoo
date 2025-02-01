# Copyright 2020 Artem Shurshilov
# Odoo Proprietary License v1.0

# This software and associated files (the "Software") may only be used (executed,
# modified, executed after modifications) if you have purchased a valid license
# from the authors, typically via Odoo Apps, or if you have received a written
# agreement from the authors of the Software (see the COPYRIGHT file).

# You may develop Odoo modules that use the Software as a library (typically
# by depending on it, importing it and using its resources), but without copying
# any source code or material from the Software. You may distribute those
# modules under the license of your choice, provided that this license is
# compatible with the terms of the Odoo Proprietary License (For example:
# LGPL, MIT, or proprietary licenses similar to this one).

# It is forbidden to publish, distribute, sublicense, or sell copies of the Software
# or modified copies of the Software.

# The above copyright notice and this permission notice must be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.


from odoo import http
from odoo.addons.iap import charge
from odoo.http import request
import requests


class MessodooController(http.Controller):
    @http.route("/send_notify", type="json", auth="none", csrf="false")
    def send_notify(self, account_token, message, device_ids):
        # the service key *is a secret*, it should not be committed in
        # the source
        service_key = request.env["ir.config_parameter"].sudo().get_param("messodoo.service_key")

        # we charge 1 credit for 1 notification FCM
        cost = 1

        # TODO: allow the user to specify how many (tens of seconds) of FCM
        with charge(http.request.env, service_key, account_token, cost):
            self._channel_firebase_notifications(message, device_ids)

    def _channel_firebase_notifications(self, message, device_ids):
        if len(device_ids) == 0:
            return
        key = request.env["ir.config_parameter"].sudo().get_param("firebase_key")
        url = "https://fcm.googleapis.com/fcm/send"

        headers = {"Content-Type": "application/json", "Authorization": "key={}".format(key)}

        if len(device_ids) > 1:
            data = {
                "notification": {
                    "title": message["author_id"][1],
                    #'subtitle': message.body,
                    "body": message["body"],
                    "sound": None,
                    "badge": None,
                },
                "dry_run": False,  # test query
                "priority": "high",
                "content_available": True,
                "registration_ids": device_ids,
            }
        else:
            data = {
                "notification": {
                    "title": message["author_id"][1],
                    #'subtitle': message.body,
                    "body": message["body"],
                    "sound": None,
                    "badge": None,
                },
                "dry_run": False,  # test query
                "priority": "high",
                "content_available": True,
                "to": ",".join(device_ids),
            }
        print(headers, data)
        answer = requests.post(url, json=data, headers=headers)
        print(answer.text)
