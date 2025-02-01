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

from odoo import models, fields, api
from odoo.addons.iap import jsonrpc


# whichever URL you deploy the service at, here we will run the remote
DEFAULT_ENDPOINT = "https://eurodoo.com"


class Channel(models.Model):
    _inherit = "mail.channel"

    @api.multi
    def _channel_message_notifications(self, message):
        """Generate the bus notifications for the given message
        :param message : the mail.message to sent
        :returns list of bus notifications (tuple (bus_channe, message_content))
        """
        res = super()._channel_message_notifications(message)

        message_values = message.message_format()[0]
        device_ids = []
        author_id = message_values["author_id"][0]

        for channel in self:
            for partner in channel.channel_partner_ids:
                if partner.id != author_id:
                    user_id = partner.user_ids and partner.user_ids[0] or False
                    if user_id and user_id.firebase_tokens:
                        device_ids = user_id.firebase_tokens.mapped("token")

        # self._channel_firebase_notifications(message_values, device_ids)
        self._send_iap_firebase_notifications(message_values, device_ids)

        return res

    # @api.multi
    # def _channel_channel_notifications(self, partner_ids):
    #     """ Generate the bus notifications of current channel for the given partner ids
    #         :param partner_ids : the partner to send the current channel header
    #         :returns list of bus notifications (tuple (bus_channe, message_content))
    #     """
    #     res = super(Channel, self)._channel_channel_notifications(partner_ids)
    #     return res

    def _send_iap_firebase_notifications(self, message, device_ids):
        # fetch the user's token for our service
        user_token = self.env["iap.account"].get("iap_firebase")

        message_json = {
            "author_id": message["author_id"],
            "body": message["body"],
        }
        params = {
            # we don't have any parameter to provide
            "account_token": user_token.account_token,
            "message": message_json,
            "device_ids": device_ids,
        }
        # ir.config_parameter allows locally overriding the endpoint
        # for testing & al
        jsonrpc(DEFAULT_ENDPOINT + "/send_notify", params=params)


class IapFirebase(models.Model):
    _name = "iap.firebase"

    user_id = fields.Many2one("res.users", string="User", readonly=True)
    os = fields.Char(string="Device OS", readonly=True)
    token = fields.Char(string="Device firebase token", readonly=True)

    _sql_constraints = [
        ("token", "unique(token, os, user_id)", "Token must be unique per user!"),
    ]


class ResUsers(models.Model):
    _inherit = "res.users"

    firebase_tokens = fields.One2many(
        "iap.firebase", "user_id", string="Firebase tokens", readonly=True
    )
