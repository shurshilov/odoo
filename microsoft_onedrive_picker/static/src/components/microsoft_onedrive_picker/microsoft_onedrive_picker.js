/**
Copyright (C) 2020-2021 Artem Shurshilov <shurshilov.a@yandex.ru>
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
odoo.define(
  "microsoft_onedrive_picker/static/src/components/microsoft_onedrive_picker/microsoft_onedrive_picker.js",
  function (require) {
    "use strict";

    // const patchMixin = require('web.patchMixin');
    // const CustomAttachmentBox = patchMixin(require('google_drive_picker/static/src/components/google_drive_picker/google_drive_picker.js'));
    const AttachmentBox = require("mail/static/src/components/attachment_box/attachment_box.js");
    const { patch } = require("web.utils");
    // const Chatter = require('mail/static/src/components/chatter/chatter.js');

    const { Component, useState } = owl;
    var core = require("web.core");
    var _t = core._t;
    var Dialog = require("web.Dialog");
    var utils = require("web.utils");

    patch(
      AttachmentBox,
      "microsoft_onedrive_picker/static/src/components/microsoft_onedrive_picker/microsoft_onedrive_picker.js",
      {
        async willStart(...args) {
          this._super(...args);
          this.config_read_onedrive = $.Deferred();
          this.onedrive = {};
          this._parseConfigOnedrive(this.env.session);
          this.config_read_onedrive.resolve();
        },

        _parseConfigOnedrive(data) {
          data = data.onedrive;
          if (data.client_id) this.onedrive.clientId = data.client_id;
          if (data.onedrive_viewType)
            this.onedrive.viewType = data.onedrive_viewType;
          if (data.onedrive_storage)
            this.onedrive.storage = data.onedrive_storage;
        },

        _copyToOdooFromOnedrive(document) {
          var deferreds = [];
          this.filesOnedrive = [];
          this.blobsOnedrive = [];
          // DOWNLOADING
          deferreds.push(this._downloadFromOnedrive(document));

          // UPLOADING
          Promise.all(deferreds).then((res) => {
            for (var i = 0; i < this.blobsOnedrive.length; i++)
              this.filesOnedrive.push(
                new File(
                  [this.blobsOnedrive[i].blob],
                  this.blobsOnedrive[i].name,
                ),
              );
            this.ondropOnedrive(this.filesOnedrive);
          });
        },

        _copyURLFromOnedrive(document) {
          this.env.services
            .rpc({
              model: "ir.attachment",
              method: "create",
              args: [
                {
                  name: document.name,
                  type: "url",
                  url: document.webUrl,
                  res_id: this.thread.id,
                  res_model: this.thread.model,
                  mimetype: document.mimetype,
                },
              ],
            })
            .then((res) => {
              this.thread.fetchAttachments.bind(this.thread)();
            });
        },

        _onMicrosoftOnedrivePicker(e) {
          this.config_read_onedrive.then((res) => {
            var picker = this.createPickerOnedrive()
              .then((result) => {
                if (result) {
                  console.log(result);
                  var def = $.Deferred();
                  if (this.onedrive.storage == "any") this._dialogStorage(def);
                  else def.resolve();
                  def.then((res) => {
                    for (const file of result.value) {
                      const name = file.name;
                      const url = file["@microsoft.graph.downloadUrl"];
                      const webUrl = file["webUrl"];
                      const mimetype = file["file"]["mimeType"];
                      const doc = {
                        name: name,
                        url: url,
                        webUrl: webUrl,
                        mimetype: mimetype,
                      };

                      if (this.onedrive.storage == "copy")
                        this._copyToOdooFromOnedrive(doc);

                      if (this.onedrive.storage == "url")
                        this._copyURLFromOnedrive(doc);
                    }
                  });
                }
              })
              .catch((reason) => {
                console.error(reason);
              });
          });
        },

        async _downloadFromOnedrive(document) {
          var def = $.Deferred();
          fetch(document.url)
            .then((response) => response.blob())
            .then((blob) => {
              this.blobsOnedrive.push({
                blob: blob,
                name: document.name,
              });
              def.resolve();
            });
          return def;
        },

        ondropOnedrive(files) {
          this._fileUploaderRef.comp.uploadFiles(files);
        },

        _setStorageOnedrive(value, def) {
          this.onedrive.storage = value;
          def.resolve();
        },

        _dialogStorage(def) {
          var self = this;
          new Dialog(this, {
            title: _t("Microsoft Onedrive select storage"),
            size: "medium",
            $content: $("<div>").html(
              _t("<p>Please, select file (files) storage:<p/>"),
            ),
            buttons: [
              {
                text: _t("Onedrive url"),
                classes: "btn-primary",
                close: true,
                click: function () {
                  self._setStorageOnedrive("url", def);
                },
              },
              {
                text: _t("Odoo copy"),
                classes: "btn-primary",
                close: true,
                click: function () {
                  self._setStorageOnedrive("copy", def);
                },
              },
              { text: _t("Cancel"), close: true },
            ],
          }).open();
        },

        // Create and render a Picker object
        createPickerOnedrive() {
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
                queryParameters:
                  "select=id,name,size,webUrl,file,folder,photo,@microsoft.graph.downloadUrl",
                createLinkParameters: { type: "edit" },
              },
              success: function (files) {
                resolve(files);
              },
              cancel: function () {
                resolve(null);
              },
              error: function (e) {
                console.log(e);
                reject(e);
              },
            };

            OneDrive.open(odOptions);
          });
        },
      },
    );
    //Chatter.components.AttachmentBox = CustomAttachmentBox;

    //return CustomAttachmentBox;
  },
);
