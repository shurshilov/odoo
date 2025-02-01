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
odoo.define('google_drive_picker', function (require) {
    "use strict";
    var core = require('web.core');
    var _t = core._t;
    var QWeb = core.qweb;
    var Chatter = require('mail.Chatter');
    var AttachmentBox = require('mail.AttachmentBox');
    //var ActionManager = require('web.ActionManager');
    var utils = require('web.utils');
    var session = require('web.session');
    var Dialog = require("web.Dialog");
    let accessToken = null;


/*    var AttachmentBox = Widget.extend({
    }):*/
    AttachmentBox.include({
        events: _.extend({}, AttachmentBox.prototype.events, {
            "click .google_drive_picker": "_onGoogleDrivePicker",           
        }),

        onPickerApiLoad:function() {
            // TODO(developer): Replace with your client ID and required scopes
            this.tokenClient = google.accounts.oauth2.initTokenClient({
            client_id: this.gdrive.clientId,
            scope: "https://www.googleapis.com/auth/drive.file",
            callback: "", // defined later
            });
          },

        init: function (parent, record, attachments) {
            var old_attachments = attachments;
            this._super.apply(this, arguments);
            attachments = old_attachments;
            var self = this;
            this.config_read = $.Deferred();
            this.cookieName = "gdrive.oauthToken";
            // Scope to use to access user's Drive items.
            this.scope = ['https://www.googleapis.com/auth/drive'];
            this.gdrive = {
                pickerApiLoaded: false,
                oauthToken: false
            };
            this._rpc({
                route: '/gdrive_picker',
                }).then( data => {
                    this._parseConfig(data);
                    this.config_read.resolve();
                    try {
                        gapi.load("picker", this.onPickerApiLoad.bind(this));
                      } catch (err) {
                        console.log("Error load Google Drive API", err);
                      }
            });
        },

        _parseConfig: function (data) {
            //this.data = data;
            if (data.client_id)
                this.gdrive.clientId = data.client_id;
            if (data.scope)
                this.gdrive.scope = [data.scope];
            else
                this.gdrive.scope = this.scope;
            if (data.mimetypes)
                this.gdrive.mimetypes = data.mimetypes;
            if (data.navbar_hidden)
                this.gdrive.navbar_hidden = data.navbar_hidden;
            if (data.locale)
                this.gdrive.locale = data.locale;
            if (data.dir)
                this.gdrive.dir = data.dir;
            if (data.gdrive_storage)
                this.gdrive.storage = data.gdrive_storage;
        },

        saveGdriveTokenCookie: function(oauthToken, expires_at) {
            utils.set_cookie(this.cookieName, oauthToken);
            utils.set_cookie('gdrive_auth2_expires_at', expires_at);
            return;
        },

        readGdriveTokenCookie: function() {
            return utils.get_cookie(this.cookieName);
        },

        readGdriveExpiresAt: function() {
            return utils.get_cookie('gdrive_auth2_expires_at');
        },

        // Create and render a Picker object for searching images.
        createPicker() {
            //debugger
            var self = this;
            if (accessToken) {
            var origin = window.location.protocol + '//' + window.location.host;
            var view = new google.picker.View(google.picker.ViewId.DOCS);
            if (this.gdrive.mimetypes)
                    view.setMimeTypes(this.gdrive.mimetypes);
            var picker = new google.picker.PickerBuilder()
                .enableFeature(google.picker.Feature.MULTISELECT_ENABLED)
                .setOAuthToken(accessToken)
                .setCallback(self.pickerCallback.bind(self))
                .setOrigin(origin)

            if (this.gdrive.navbar_hidden)
                    picker.enableFeature(google.picker.Feature.NAV_HIDDEN)

            if (this.gdrive.locale)
                    picker.setLocale(this.gdrive.locale)

            picker.addView(view);
            picker.addView(new google.picker.DocsUploadView().setIncludeFolders(true));
            if (this.gdrive.dir) {
                    picker.addView(new google.picker.DocsView().setParent(this.gdrive.dir))
                    picker.addView(new google.picker.DocsUploadView().setParent(this.gdrive.dir).setIncludeFolders(true))
            }
/*            else {
                picker.addView(view);
                picker.addView(new google.picker.DocsUploadView().setIncludeFolders(true));
            }*/
            picker.addView(google.picker.ViewId.DOCUMENTS);

             picker.build().setVisible(true);
          }
        },

        _downloadFromGdrive: async function (document) {
            var def = $.Deferred();
            let url = 'https://www.googleapis.com/drive/v2/files/' + document.id+ '?alt=media&source=downloadUrl';
            let headers = {headers: {'Authorization': 'Bearer ' + this.gdrive.oauthToken}};
            fetch(url, headers).then( response =>{
                response.blob().then( blob =>{
                    this.blobsGdrive.push({
                        blob: blob,
                        name: document.name
                    });
                    def.resolve();
                })
            })
            return def;
        },

        _copyToOdooFromGdrive: function (document){
            var deferreds = [];
            this.filesGdrive = [];
            this.blobsGdrive = [];
            // DOWNLOADING
            deferreds.push(this._downloadFromGdrive(document));

            // UPLOADING
            Promise.all(deferreds).then( res => {
                for (var i = 0; i < this.blobsGdrive.length; i++)
                       this.filesGdrive.push( new File([this.blobsGdrive[i].blob], this.blobsGdrive[i].name) );
                this.ondropGdrive(this.filesGdrive);
            });
        },

        _copyURLFromGdrive: function (document){
            this._rpc({
                model: 'ir.attachment',
                method: 'create',
                args: [{'name': document.name,
                        'type': 'url',
                        //'type': 'gdrive',
                        'url': document.url,
                        'res_id': this.currentResID,
                        'res_model': this.currentResModel,
                        'mimetype': document.mimeType
                    }],
            }).then( res =>{
                this.trigger_up('reload_attachment_box');
            })
        },

        pickerCallback: function(data) {
            var self = this;
            var url = 'nothing';
            if (data[google.picker.Response.ACTION] == google.picker.Action.PICKED) {
                var def = $.Deferred();
                if (this.gdrive.storage == 'any')
                    this._dialogStorageGdrive(def);
                else
                        def.resolve();
                def.then( res =>{
                        // SELECT DOCUMENTS
                        var docs = data[google.picker.Response.DOCUMENTS]
                        var documents = [];
                        for (var i = 0; i < docs.length; i++) {
                            var doc = docs[i];
                            documents.push({
                                id: doc[google.picker.Document.ID],
                                name: doc[google.picker.Document.NAME],
                                url: doc[google.picker.Document.EMBEDDABLE_URL] || doc[google.picker.Document.URL]
                            });

                            if (this.gdrive.storage == 'copy')
                                this._copyToOdooFromGdrive(doc);

                            if (this.gdrive.storage == 'url')
                                this._copyURLFromGdrive(doc);
                        }
                });
            }
        },

        _setStorageGdrive: function(value, def){
            this.gdrive.storage = value;
            def.resolve();
        },

        _dialogStorageGdrive: function(def){
            var self = this;
            new Dialog(this, {
                title: _t('Google Drive select storage'),
                size: 'medium',
                $content: $('<div>').html(_t('<p>Please, select file (files) storage:<p/>')),
                buttons: [
                {text: _t('Google Drive url'), classes: 'btn-primary', close: true, click: function () {self._setStorageGdrive('url', def)}},
                {text: _t('Odoo copy'), classes: 'btn-primary', close: true, click: function () {self._setStorageGdrive('copy', def)}},
                {text: _t('Cancel'), close: true}]
            }).open()
        },



        generate_access_token() {
            const generate_access_token_done = $.Deferred();
            this.tokenClient.callback = async (response) => {
              if (response.error !== undefined) {
                throw response;
              }
              accessToken = response.access_token;
              generate_access_token_done.resolve(accessToken);
            };
  
            if (accessToken === null) {
              // Prompt the user to select a Google Account and ask for consent to share their data
              // when establishing a new session.
              this.tokenClient.requestAccessToken({ prompt: "consent" });
            } else {
              // Skip display of account chooser and consent dialog for an existing session.
              this.tokenClient.requestAccessToken({ prompt: "" });
            }
            return generate_access_token_done;
          },

          async _onGoogleDrivePicker(e) {
            try {
              // wait access token, then open picker
              accessToken = await this.generate_access_token();
              await this.createPicker();
            } catch (err) {
              console.log("Error load Google Drive API", err);
            }
          },

        ondropGdrive: function (files){
             var self = this;
                 var form_upload = document.querySelector('form.o_form_binary_form');
                 if (form_upload.length == 0) {
                     return;
                 }

                 var form_data = new FormData(form_upload);
                 for (var iterator = 0, file; file = files[iterator]; iterator++) {
                     form_data.set('ufile', file);

                     $.ajax({
                         url: form_upload.getAttribute('action'),
                         method: form_upload.getAttribute('method'),
                         type: form_upload.getAttribute('method'),
                         processData: false,
                         contentType: false,
                         data: form_data,
                         success: function (data) {
                             self.trigger_up('reload_attachment_box');
                         },
                         error: function (jqXHR, textStatus, errorThrown) {
                             console.error(jqXHR, textStatus, errorThrown);
                         }
                     });
                 }
         },
    });

/*    Chatter.include({
        _fetchAttachments: function () {
            var self = this;
            var domain = [
                ['res_id', '=', this.record.res_id],
                ['res_model', '=', this.record.model],
            ];
            return this._rpc({
                model: 'ir.attachment',
                method: 'search_read',
                domain: domain,
                fields: ['id', 'name', 'mimetype', 'create_uid', 'create_date', 'file_size', 'public', 'type', 'url'],
            }).then(function (result) {
                self._areAttachmentsLoaded = true;
                self.attachments = result;
                _.each(self.attachments, function (attachment) {
                    attachment.file_size = utils.human_size(attachment.file_size);
                    attachment.public = attachment.public;
                    attachment.create_uid = attachment.create_uid;
                    attachment.type = attachment.type;
                    attachment.weburl = attachment.url;
                });

            });

        },
    });*/
/*    ActionManager.include({
        _handleAction: function (action, options) {
            if (action.type === 'ir.actions.act_close_wizard_and_reload_attachments') {
                return this.ir_actions_act_close_wizard_and_reload_attachments();
            }
            return this._super(action, options);
        },

        ir_actions_act_close_wizard_and_reload_attachments: function (action, options) {
           this._closeDialog();
           this.getCurrentController().widget.renderer.chatter._onReloadAttachmentBox();
        },
    });*/

});
        