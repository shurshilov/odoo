/** @odoo-module */

import { ChatterTopbar } from "@mail/components/chatter_topbar/chatter_topbar";
import { patch } from "web.utils";
import Dialog from "web.Dialog";
import core from "web.core";
const _t = core._t;
import { session } from "@web/session";

patch(ChatterTopbar.prototype, "microsoft_onedrive_picker", {
  setup() {
    this._super(...arguments);
    this.config_read_onedrive = $.Deferred();
    this.cookieName = "gdrive.oauthToken";
    // Scope to use to access user's Drive items.
    this.scope = "https://www.googleapis.com/auth/drive.file";
    this.onedrive = {};
    console.log(session);
    this._parseConfigOnedrive(session);
    this.config_read_onedrive.resolve();
  },

  _parseConfigOnedrive(data) {
    data = data.onedrive;
    if (data.client_id) this.onedrive.clientId = data.client_id;
    if (data.onedrive_viewType) this.onedrive.viewType = data.onedrive_viewType;
    if (data.onedrive_storage) this.onedrive.storage = data.onedrive_storage;
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
          new File([this.blobsOnedrive[i].blob], this.blobsOnedrive[i].name),
        );
      this.ondropOnedrive(this.filesOnedrive);
    });
  },

  _copyURLFromOnedrive(document) {
    this.messaging
      .rpc({
        model: "ir.attachment",
        method: "create",
        kwargs: {
          vals_list: [
            {
              name: document.name,
              type: "url",
              url: document.webUrl,
              res_id: this.props.record.chatter.thread.id,
              res_model: this.props.record.chatter.thread.model,
              mimetype: document.mimeType,
            },
          ],
        },
      })
      .then((res) => {
        this.props.record.chatter.refresh();
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

  async ondropOnedrive(files) {
    await this.props.record.chatter.fileUploader.uploadFiles(files);
    this.props.record.chatter.refresh();
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
        // openInNewWindow: true,
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
});
