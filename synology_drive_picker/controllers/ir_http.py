# -*- coding: utf-8 -*-
# Copyright (C) 2020 Artem Shurshilov <shurshilov.a@yandex.ru>
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
from odoo import models
from odoo.http import request
from ..models.synology_api import filestation, downloadstation
from datetime import datetime
from odoo.exceptions import UserError
import logging
logger = logging.getLogger(__name__)


class Http(models.AbstractModel):
    _inherit = 'ir.http'

    def session_info(self):
        """ Params for dynamic interface
        """
        result = super(Http, self).session_info()
        cp = request.env['res.users'].sudo().browse(request.env.user.id)

        if (datetime.now() - cp.write_date).seconds > 60*60*24*7 or not cp.synology_session:
            if not cp.synology_ip or not cp.synology_port or not cp.synology_user or not cp.synology_pass:
                UserError("Please check user synology settings")
            try:
                fl = filestation.FileStation(cp.synology_ip, cp.synology_port, cp.synology_user,
                                             cp.synology_pass, cp.synology_https)
                cp.synology_session = fl._sid
            except Exception as e:
                logger.warning("Synology FileStation error '%s'", e)
                return result

        result['synology_sid'] = cp.synology_session
        return result
