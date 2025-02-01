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
odoo.define('microsoft_onedrive_picker_discuss', function (require) {
    "use strict";
    var core = require('web.core');
    var _t = core._t;
    var QWeb = core.qweb;
    //var Chatter = require('mail.Chatter');
    //var AttachmentBox = require('mail.AttachmentBox');
    //var ActionManager = require('web.ActionManager');
    var Discuss = require('mail.Discuss');
    var Dialog = require("web.Dialog");
    var utils = require('web.utils');
    //var session = require('web.session');
    var BasicComposer = require('mail.composer.Basic');
    BasicComposer.include({
    /**
     * Allowing to upload attachment with file selector as well drag drop feature.
     *
     * @private
     * @param {Array<File>} params.files
     * @param {boolean} params.submitForm [optional]
     */
    _processAttachmentChange: function (params) {
        var self = this;
        var attachments = this.get('attachment_ids');
        var files = params.files;
        var submitForm = params.submitForm;
        var $form = this.$('form.o_form_binary_form');

        /**
         * makes a new formData as formData.delete() is not supported by IE or Safari Mobile.
         *
         * @return {FormData}
         */
        function makeFormDataWithoutUfile() {
            var newFormData = new window.FormData();
            $form.find('input').each(function (index, input) {
                if (input.name !== 'ufile') {
                    newFormData.append(input.name, input.value);
                }
            });
            return newFormData;
        }

        _.each(files, function (file) {
            var attachment = _.findWhere(attachments, {
                name: file.name,
                size: file.size
            });
            // if the files already exits, delete the file before upload
            if (attachment) {
                self._attachmentDataSet.unlink([attachment.id]);
                attachments = _.without(attachments, attachment);
            }
        });

        if (submitForm) {
            $form.submit();
            this._$attachmentButton.prop('disabled', true);
        } else {
            _.each(files, function (file) {
                console.log(file)
                var formData = makeFormDataWithoutUfile();
                formData.append("ufile", file, file.name);
                $.ajax({
                    url: $form.attr("action"),
                    type: "POST",
                    enctype: 'multipart/form-data',
                    processData: false,
                    contentType: false,
                    data: formData,
                    success: function (result) {
                        var $el = $(result);
                        $.globalEval($el.contents().text());
                    }
                });
            });
        }
        var uploadAttachments = _.map(files, function (file){
            return {
                id: 0,
                name: file.name,
                filename: file.name,
                url: '',
                upload: true,
                mimetype: '',
            };
        });
        attachments = attachments.concat(uploadAttachments);
        this.set('attachment_ids', attachments);
    },
    });


    Discuss.include({
        events: _.extend({}, Discuss.prototype.events, {
            "click .microsoft_onedrive_picker": "_onMicrosoftOnedrivePicker",           
        }),

        init: function (parent, record, attachments) {
            this._super.apply(this, arguments);
            var self = this;
            this.config_read_onedrive = $.Deferred();
            this._rpc({
                route: '/onedrive_picker',
                }).then( data => {
                    this._parseConfigOnedrive(data);
                    this.config_read_onedrive.resolve();
            });

            this.onedrive = {};
        },

        _parseConfigOnedrive: function (data) {
            if (data.client_id)
                this.onedrive.clientId = data.client_id;
            if (data.onedrive_viewType)
                this.onedrive.viewType = data.onedrive_viewType;
            if (data.onedrive_storage)
                this.onedrive.storage = data.onedrive_storage;
        },

        _copyToOdooFromOnedrive: function (document){
            var deferreds = [];
            this.filesOnedrive = [];
            this.blobsOnedrive = [];
            // DOWNLOADING
            deferreds.push(this._downloadFromOnedrive(document));

            // UPLOADING
            Promise.all(deferreds).then( res => {
                for (var i = 0; i < this.blobsOnedrive.length; i++)
                       this.filesOnedrive.push( new File([this.blobsOnedrive[i].blob], this.blobsOnedrive[i].name) );
                this.ondropOnedrive(this.filesOnedrive);
            });
        },

        _copyURLFromOnedrive: function (document){
            this._rpc({
                model: 'ir.attachment',
                method: 'create',
                args: [{'name': document.name,
                        'type': 'url',
                        'url': document.webUrl,
                        'res_id': this.currentResID,
                        'res_model': this.currentResModel,
                        'mimetype': document.mimetype
                    }],
            }).then( res =>{
                //this.trigger_up('reload_attachment_box');
            })
        },

        _onMicrosoftOnedrivePicker: function(e) {
            this.config_read_onedrive.then( res =>{
                var picker = this.createPickerOnedrive().then( result =>{
                    if (result) {
                        console.log(result);
                        var def = $.Deferred();
                        if (this.onedrive.storage == 'any')
                                this._dialogStorage(def);
                        else
                            def.resolve();
                        def.then( res =>{
                            for (const file of result.value) {
                                const name = file.name;
                                const url = file["@microsoft.graph.downloadUrl"];
                                const webUrl = file["webUrl"];
                                const mimetype = file["file"]["mimeType"];
                                const doc = { name: name, url: url, webUrl: webUrl, mimetype: mimetype };

                                if (this.onedrive.storage == 'copy')
                                    this._copyToOdooFromOnedrive(doc);

                                if (this.onedrive.storage == 'url')
                                    this._copyURLFromOnedrive(doc);  
                            }
                        })
                    }
                }).catch(reason => {
                    console.error(reason);
                });     
            });
        },

        _downloadFromOnedrive: async function (document) {
            var def = $.Deferred();
            fetch(document.url).then(response => response.blob())
                .then(blob => {
                        this.blobsOnedrive.push({
                            blob: blob,
                            name: document.name
                        });
                        def.resolve();
                });
            return def;
        },

        ondropOnedrive: function (files){
            this._basicComposer._processAttachmentChange({
                files: files,
                submitForm: false
            });
            return;
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
                         //self.trigger_up('reload_attachment_box');
                     },
                     error: function (jqXHR, textStatus, errorThrown) {
                         console.error(jqXHR, textStatus, errorThrown);
                     }
                 });
             }
         },

        _setStorageOnedrive: function(value, def){
            this.onedrive.storage = value;
            def.resolve();
        },

        _dialogStorage: function(def){
            var self = this;
            new Dialog(this, {
                title: _t('Microsoft Onedrive select storage'),
                size: 'medium',
                $content: $('<div>').html(_t('<p>Please, select file (files) storage:<p/>')),
                buttons: [
                {text: _t('Onedrive url'), classes: 'btn-primary', close: true, click: function () {self._setStorageOnedrive('url', def)}},
                {text: _t('Odoo copy'), classes: 'btn-primary', close: true, click: function () {self._setStorageOnedrive('copy', def)}},
                {text: _t('Cancel'), close: true}]
            }).open()
        },

        // Create and render a Picker object
        createPickerOnedrive: function() {
            return new Promise((resolve, reject) => {
            var odOptions = {
                clientId: this.onedrive.clientId,
                //action: "download",
                action: "query",
                //action: "share",
                multiSelect: true,
                openInNewWindow: true,
                viewType: this.onedrive.viewType, //folders, files
                advanced: {
                    queryParameters: "select=id,name,size,webUrl,file,folder,photo,@microsoft.graph.downloadUrl",
                    createLinkParameters: { type: "edit" }
                },
                success: function (files) { resolve(files); },
                cancel: function () { resolve(null); },
                error: function (e) { console.log(e); reject(e); }
            };

            OneDrive.open(odOptions);
            });
        },

    });

});
        