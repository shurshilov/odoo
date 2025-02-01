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
odoo.define("dropbox_picker", function (require) {
  "use strict";

  const AttachmentBox = require("mail/static/src/components/attachment_box/attachment_box.js");
  const { patch } = require("web.utils");
  const { Component, useState } = owl;
  var core = require("web.core");
  var _t = core._t;
  var Dialog = require("web.Dialog");
  var utils = require("web.utils");

  //AttachmentBox.include({
  patch(AttachmentBox, "dropbox_picker", {
    async willStart(...args) {
      this._super(...args);
      var self = this;
      this.config_read_dropbox = $.Deferred();
      this.env.services
        .rpc({
          route: "/dropbox_picker",
        })
        .then((data) => {
          this._parseConfigDropbox(data);
          this.config_read_dropbox.resolve();
        });

      this.dropbox = {};
    },

    _parseConfigDropbox(data) {
      if (data.client_id) this.dropbox.clientId = data.client_id;
      if (data.dropbox_storage) this.dropbox.storage = data.dropbox_storage;
    },

    _copyToOdooFromDropbox(document) {
      var deferreds = [];
      this.filesDropbox = [];
      this.blobsDropbox = [];
      // DOWNLOADING
      deferreds.push(this._downloadFromDropbox(document));

      // UPLOADING
      Promise.all(deferreds).then((res) => {
        for (var i = 0; i < this.blobsDropbox.length; i++)
          this.filesDropbox.push(
            new File([this.blobsDropbox[i].blob], this.blobsDropbox[i].name),
          );
        this.ondropDropbox(this.filesDropbox);
      });
    },

    _copyURLFromDropbox(document) {
      this.env.services
        .rpc({
          model: "ir.attachment",
          method: "create",
          args: [
            {
              name: document.name,
              type: "url",
              url: document.link,
              res_id: this.thread.id,
              res_model: this.thread.model,
              //'mimetype': document.mimetype
            },
          ],
        })
        .then((res) => {
          this.thread.fetchAttachments.bind(this.thread)();
        });
    },

    _onDropboxPicker(e) {
      this.config_read_dropbox.then((res) => {
        var def = $.Deferred();
        if (this.dropbox.storage == "any") this._dialogStorageDropbox(def);
        else def.resolve();
        def.then((res) => {
          var picker = this.createPickerDropbox().then((result) => {
            if (result) {
              console.log(result);
              for (const file of result) {
                if (this.dropbox.storage == "copy")
                  this._copyToOdooFromDropbox(file);

                if (this.dropbox.storage == "url")
                  this._copyURLFromDropbox(file);
              }
            }
          });
        });
      });
    },

    async _downloadFromDropbox(document) {
      var def = $.Deferred();
      fetch(document.link)
        .then((response) => response.blob())
        .then((blob) => {
          this.blobsDropbox.push({
            blob: blob,
            name: document.name,
          });
          def.resolve();
        });
      return def;
    },

    ondropDropbox(files) {
      this._fileUploaderRef.comp.uploadFiles(files);
      //  var self = this;
      //  var form_upload = document.querySelector('form.o_form_binary_form');
      //  if (form_upload.length == 0) {
      //      return;
      //  }

      //  var form_data = new FormData(form_upload);
      //  for (var iterator = 0, file; file = files[iterator]; iterator++) {
      //      form_data.set('ufile', file);

      //      $.ajax({
      //          url: form_upload.getAttribute('action'),
      //          method: form_upload.getAttribute('method'),
      //          type: form_upload.getAttribute('method'),
      //          processData: false,
      //          contentType: false,
      //          data: form_data,
      //          success: function (data) {
      //              self.trigger_up('reload_attachment_box');
      //          },
      //          error: function (jqXHR, textStatus, errorThrown) {
      //              console.error(jqXHR, textStatus, errorThrown);
      //          }
      //      });
      //  }
    },

    _setStorageDropbox(value, def) {
      this.dropbox.storage = value;
      def.resolve();
    },

    _dialogStorageDropbox(def) {
      var self = this;
      new Dialog(this, {
        title: _t("Dropbox select storage"),
        size: "medium",
        $content: $("<div>").html(
          _t("<p>Please, select file (files) storage:<p/>"),
        ),
        buttons: [
          {
            text: _t("Dropbox url"),
            classes: "btn-primary",
            close: true,
            click: function () {
              self._setStorageDropbox("url", def);
            },
          },
          {
            text: _t("Odoo copy"),
            classes: "btn-primary",
            close: true,
            click: function () {
              self._setStorageDropbox("copy", def);
            },
          },
          { text: _t("Cancel"), close: true },
        ],
      }).open();
    },

    // Create and render a Picker object
    createPickerDropbox() {
      var def = $.Deferred();
      var options = {
        // Required. Called when a user selects an item in the Chooser.
        success: function (files) {
          def.resolve(files);
        },

        // Optional. Called when the user closes the dialog without selecting a file
        // and does not include any parameters.
        cancel: function () {
          def.resolve();
        },

        // Optional. "preview" (default) is a preview link to the document for sharing,
        // "direct" is an expiring link to download the contents of the file. For more
        // information about link types, see Link types below.
        linkType: this.dropbox.storage == "url" ? "preview" : "direct", // or "direct"

        // Optional. A value of false (default) limits selection to a single file, while
        // true enables multiple file selection.
        multiselect: true, // or true

        // Optional. This is a list of file extensions. If specified, the user will
        // only be able to select files with these extensions. You may also specify
        // file types, such as "video" or "images" in the list. For more information,
        // see File types below. By default, all extensions are allowed.
        //extensions: ['.pdf', '.doc', '.docx'],

        // Optional. A value of false (default) limits selection to files,
        // while true allows the user to select both folders and files.
        // You cannot specify `linkType: "direct"` when using `folderselect: true`.
        folderselect: false, // or true

        // Optional. A limit on the size of each file that may be selected, in bytes.
        // If specified, the user will only be able to select files with size
        // less than or equal to this limit.
        // For the purposes of this option, folders have size zero.
        //sizeLimit: 1024, // or any positive number
      };

      Dropbox.choose(options);
      return def;
    },
  });
});
