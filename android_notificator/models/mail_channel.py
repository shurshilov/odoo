# -*- coding: utf-8 -*-
# Copyright 2020-2022 Artem Shurshilov
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

from odoo import models, _
import requests
from odoo.exceptions import UserError, ValidationError


class Channel(models.Model):
    _inherit = 'mail.channel'

    def _channel_message_notifications(self, message, message_format=False):
        """ Generate the bus notifications for the given message
            :param message : the mail.message to sent
            :returns list of bus notifications (tuple (bus_channe, message_content))
        """
        res = super(Channel, self)._channel_message_notifications(
            message, message_format=message_format)

        if self.env['ir.config_parameter'].sudo().get_param('firebase_channel_notify'):
            message_values = message.message_format()[0]
            device_ids = []
            author_id = message_values['author_id'][0]

            for channel in self:
                for partner in channel.channel_partner_ids:
                    if partner.id != author_id:
                        user_id = partner.user_ids and partner.user_ids[0] or False
                        if user_id and user_id.mail_firebase_tokens:
                            device_ids += user_id.mail_firebase_tokens.mapped('token')
            device_ids = list(set(device_ids))
            # sending firebase push notifications
            self._prepare_firebase_notifications(message_values, device_ids)

        return res

    def _prepare_firebase_notifications(self, message, device_ids):
        """
            Prepare message before send
            {'id': 2323,
            'body': '<p>123</p>',
            'date': datetime.datetime(2020, 11, 19, 19, 41, 48),
            'author_id': (47, 'demo1'),
            'email_from': '"demo1" <notfound@gmail.com>',
            'message_type': 'comment',
            'subtype_id': (1, 'Discussions'),
            'subject': False,
            'model': 'mail.channel',
            'res_id': 30,
            'record_name':
            'demo1, Artem Shurshilov',
            'channel_ids': [30],
            'partner_ids': [],
            'starred_partner_ids': [],
            'moderation_status': 'accepted',
            'customer_email_status': 'sent',
            'customer_email_data': [],
            'attachment_ids': [],
            'tracking_value_ids': [],
            'needaction_partner_ids': [],
            'is_note': False,
            'is_discussion': True,
            'is_notification': False,
            'subtype_description': False,
            'module_icon': '/mail/static/description/icon.png'}
        """
        message_json = {
            'author_id': message['author_id'],
            # delete <p></p>
            'body': message['body'][3:-4],
            'body_html': message['body'],
            'channel_ids': message['channel_ids'],
        }
        self._mail_channel_firebase_notifications(message_json, device_ids)

    def _mail_channel_firebase_notifications(self, message, device_ids):
        """
            Send notifications via Firebase Cloud
        """
        if len(device_ids) == 0:
            return
        # key = "AAAAmsbwHC4:APA91bHOpTMKFkbZ5qhAVFsb0Qgk2Hsgh3H_oYh_8xxYleJzGm0LHcljtcUYBP-KWmB5hITRrLFEHLJOphWSwLUr9Qtr4md3VdTKu8_tHl7k69RmfIaAiCj88fJisRmWVJACyChGKJYf"
        key = self.env['ir.config_parameter'].sudo(
        ).get_param('mail_firebase_key')
        if not key:
            return
        url = 'https://fcm.googleapis.com/fcm/send'

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'key={}'.format(key)
        }

        # https://firebase.google.com/docs/reference/admin/python/firebase_admin.messaging
        if len(device_ids) > 1:
            data = {
                "notification": {
                    'title': message['author_id'][1],
                    'subtitle': message['channel_ids'],
                    'body': message['body'],
                    'sound': None,
                    'badge': None,
                    # 'icon': 'https://firebase.google.com/downloads/brand-guidelines/SVG/logo-vertical.svg',
                    'icon': 'https://firebase.google.com/downloads/brand-guidelines/PNG/logo-vertical.png',
                    # 'image': 'https://firebase.google.com/downloads/brand-guidelines/SVG/logo-vertical.svg',
                    # 'click_action':
                },
                'dry_run': False,  # test query
                'priority': 'high',
                'content_available': True,
                "data": {
                    "channel_ids": message['channel_ids'],
                    "body_html": message['body_html']

                },
                "registration_ids": device_ids,
            }
        else:
            data = {
                "notification": {
                    'title': message['author_id'][1],
                    'subtitle': message['channel_ids'],
                    'data': message['channel_ids'],
                    'body': message['body'],
                    'sound': None,
                    'badge': None,
                    # 'icon': 'https://firebase.google.com/downloads/brand-guidelines/SVG/logo-vertical.svg',
                    'icon': 'https://firebase.google.com/downloads/brand-guidelines/PNG/logo-vertical.png',
                    # 'image': 'https://firebase.google.com/downloads/brand-guidelines/SVG/logo-vertical.svg',
                },
                'dry_run': False,  # test query
                'priority': 'high',
                'content_available': True,
                "data": {
                    "channel_ids": message['channel_ids'],
                    "body_html": message['body_html']
                },
                "to": ','.join(device_ids),
            }
        answer = requests.post(url, json=data, headers=headers)
