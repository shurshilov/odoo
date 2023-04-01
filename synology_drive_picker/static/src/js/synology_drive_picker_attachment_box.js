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
odoo.define('synology_drive_picker', function (require) {
    "use strict";
    var core = require('web.core');
    var _t = core._t;
    var QWeb = core.qweb;
    var Chatter = require('mail.Chatter');
    var AttachmentBox = require('mail.AttachmentBox');

    var utils = require('web.utils');
    var session = require('web.session');
    var Dialog = require("web.Dialog");

    AttachmentBox.include({
        events: _.extend({}, AttachmentBox.prototype.events, {
            "click .synology_drive_picker": "_onSynologyDrivePicker",           
        }),

        _onSynologyRequest: function (funcAPT='get_info', params_list=[]) {
            console.log('params_list', params_list)
            return this._rpc({
                    model: 'ir.attachment',
                    method: 'synology',
                    kwargs: {
                        funcAPI: funcAPT,
                        params_list: params_list,
                    },
                })
        },
        _onSynologyDrivePicker: function (ev) {
            ev.stopPropagation();
            ev.preventDefault();
            this._onSynologyTree(false, ev);
        },

        _onSynologyImport: function (ev) {
            ev.stopPropagation();
            ev.preventDefault();
            let path = $(ev.target).data('path');
            console.log('import_path', path)
            this._rpc({
                    model: 'ir.attachment',
                    method: 'synology_import',
                    kwargs: {
                        path: path,
                        res_model: this.getParent().context.default_model,
                        res_id: this.getParent().context.default_res_id,

                    },
            }).then( res =>{
                this.trigger_up('reload_attachment_box');
            });
            
        },

		_onAttachmentDownload: function (ev) {
            ev.stopPropagation();
            ev.preventDefault();
            this._onDownloadAttachment(ev);
		},

        _onDownloadAttachment: function (ev) {
            ev.stopPropagation();
            ev.preventDefault();
            var activeAttachmentID = $(ev.currentTarget).data('id');
            var attachmentObject = {};
            _.each(this.attachmentIDs, function (attachment) {
                if (attachment.id === activeAttachmentID){
                    attachmentObject = attachment;
                    return
                }
            });

            // if synology file
            if (attachmentObject.weburl && attachmentObject.weburl.indexOf('SYNO.FileStation.Download') != -1 ){
                //window.open(, '_blank');
                window.location.href = attachmentObject.weburl.replace('mode=open','mode=download') + session.synology_sid;
                return;
            }
            
            window.location.href = attachmentObject.url;
            //this._super.apply(this, arguments);
        },

        _onAttachmentView: function (ev) {
            ev.stopPropagation();
            ev.preventDefault();
            var activeAttachmentID = $(ev.currentTarget).data('id');
            var attachmentObject = {};
            _.each(this.attachmentIDs, function (attachment) {
                if (attachment.id === activeAttachmentID){
                    attachmentObject = attachment;
                    return
                }
            });

            // if synology file
            if (attachmentObject.weburl && attachmentObject.weburl.indexOf('SYNO.FileStation.Download') != -1 ){
                window.open(attachmentObject.weburl + session.synology_sid, '_blank');
                return;
            }

            this._super.apply(this, arguments);
        },

        _onSynologyDownload: function (ev) {
            ev.stopPropagation();
            ev.preventDefault();
            let path = $(ev.target).data('path');

            this._rpc({
                    model: 'ir.attachment',
                    method: 'synology_download',
                    kwargs: {
                        path: path,
                    },
            }).then( url =>{
                window.location.href = url;
                //window.open(url, '_blank');
            });
        },

        _onSynologyTree: async function (mode, ev) {
            let path = $(ev.target).data('path');
            if (mode == 'back'){
                let lastIndex=this.res[0].path.lastIndexOf("/");
                path=this.res[0].path.slice(0,lastIndex);
                lastIndex=path.lastIndexOf("/");
                path=path.slice(0,lastIndex);

            }

            if (!path){
                this.res = await this._onSynologyRequest('get_list_share');
                this.res = this.res.data.shares;
                var AttachmentInfo = $(QWeb.render("SynologyTree", {files: this.res, back: false}));
                console.log('res')
                console.log(this.res)
            }
            else{
                this.res = await this._onSynologyRequest('get_file_list', [path]);
                this.res = this.res.data.files;
                var AttachmentInfo = $(QWeb.render("SynologyTree", {files: this.res, back: true}));
                console.log('res')
                console.log(this.res)
            }

            if (this.popup_preview)
                this.popup_preview.close();
            
            this.popup_preview = new Dialog(this, {
                size: 'large',
                dialogClass: 'o_act_window',
                title: _t("Attachments synology picker"),
                $content: AttachmentInfo,
                buttons: [
                    {
                        text: _t("Close"), close: true
                    }
                ]
            }).open();

            AttachmentInfo.find('.folder').on('click', this._onSynologyTree.bind(this, 'forward'));
            AttachmentInfo.find('.file').on('click', this._onSynologyTree.bind(this, 'forward'));
            AttachmentInfo.find('.oe_button_import_from_synology').on('click', this._onSynologyImport.bind(this));
            AttachmentInfo.find('.oe_button_download_from_synology').on('click', this._onSynologyDownload.bind(this));
            AttachmentInfo.find('.oe_button_back').on('click', this._onSynologyTree.bind(this,'back'));
        },
    });
});
        