/**
Copyright (C) 2020 Artem Shurshilov <shurshilov.a@yandex.ru>
Odoo Proprietary License v1.0

This software and associated files (the "Software") may only be used (executed,
modified, executed after modifications) if you have purchased a valid license
from the authors, typically via Odoo Apps, or if you have received a written
agreement from the authors of the Software (see the COPYRIGHT file).

You may develop Odoo modules that use the Software as a library (typically
by depending on it, importing it and using its resources), but without copying
any source code or material from the Software. You may distribute those
modules under the license of your choice, provided that this license is
compatible with the terms of the Odoo Proprietary License (For example:
LGPL, MIT, or proprietary licenses similar to this one).

It is forbidden to publish, distribute, sublicense, or sell copies of the Software
or modified copies of the Software.

The above copyright notice and this permission notice must be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.**/
odoo.define('attachments_preview_ms_and_google', function (require) {
    "use strict";
    var core = require('web.core');
    var _t = core._t;
    var QWeb = core.qweb;
    var Chatter = require('mail.Chatter');
    var ActionManager = require('web.ActionManager');
    var AttachmentBox = require('mail.AttachmentBox');
    var ListView = require('web.ListView');
    var rpc = require('web.rpc');
    var utils = require('web.utils');
    var Dialog = require('web.Dialog');
    var session = require('web.session');

    // ATTACHMENTS EDIT AND PREVIEW
    AttachmentBox.include({
        events: _.extend({}, AttachmentBox.prototype.events, {
            'click .o_attachment_preview_ms_cross': '_onPreviewMSAttachment',
            'click .o_attachment_preview_google_cross': '_onPreviewGoogleAttachment',
        }),

        _onPreviewMSAttachment: function (ev) {
            ev.stopPropagation();
            ev.preventDefault();
            var activeAttachmentURL = $(ev.currentTarget).data('url');
            var url = 'https://view.officeapps.live.com/op/embed.aspx?src='+
            window.location.origin + activeAttachmentURL;
            window.open(url, '_blank');
        },

        _onPreviewGoogleAttachment: function (ev) {
            ev.stopPropagation();
            ev.preventDefault();
            var activeAttachmentURL = $(ev.currentTarget).data('url');
            var url = 'https://docs.google.com/viewer?url='+
            window.location.origin + activeAttachmentURL;
            window.open(url, '_blank');
        },

    });

});
