# -*- coding: utf-8 -*-
# Copyright 2021 Artem Shurshilov
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
from odoo import fields, models, api

class MailThread(models.AbstractModel):
    _inherit = "mail.thread"

    @api.returns('mail.message', lambda value: value.id)
    def message_post(self, **kwargs):
        if not self._context.get('auto_subscribe_recipients'):
            return super(MailThread, self.with_context(mail_post_autofollow=False)).message_post(**kwargs)
        return super().message_post(**kwargs)


class MailComposer(models.TransientModel):
    _inherit = 'mail.compose.message'

    auto_subscribe_recipients = fields.Boolean(
        string='Auto subscribe recipients')

    def _action_send_mail(self, **kwargs):
        for wizard in self:
            self = self.with_context(auto_subscribe_recipients=wizard.auto_subscribe_recipients)
        return super(MailComposer, self)._action_send_mail(**kwargs)
