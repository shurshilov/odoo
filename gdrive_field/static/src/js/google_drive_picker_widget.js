/* @odoo-module */
import { registry } from "@web/core/registry";
import { session } from "@web/session";
import Dialog from "web.Dialog";
import core from "web.core";
const _t = core._t;
const { xml, Component, onMounted, onWillStart } = owl;
import { standardFieldProps } from "@web/views/fields/standard_field_props";
// import { loadBundle, loadJS } from "@web/core/assets";
import { useService } from "@web/core/utils/hooks";
// Add the field to the correct category

export class FieldGoogleDrivePicker extends Component {
  setup() {
    // this._super(...arguments);
    this.rpc = useService("rpc");
    this.config_read = $.Deferred();
    // Scope to use to access user's Drive items.
    this.scope = "https://www.googleapis.com/auth/drive.file";
    this.gdrive = {
      pickerApiLoaded: false,
      oauthToken: false,
    };
    console.log(session);
    this._parseConfig(session);
    this.config_read.resolve();
  }

  _parseConfig(data) {
    data = data.gdrive;
    if (data.client_id) this.gdrive.clientId = data.client_id;
    if (data.scope) this.gdrive.scope = data.scope;
    else this.gdrive.scope = this.scope;
    if (data.mimetypes) this.gdrive.mimetypes = data.mimetypes;
    if (data.navbar_hidden) this.gdrive.navbar_hidden = data.navbar_hidden;
    if (data.locale) this.gdrive.locale = data.locale;
    if (data.dir) this.gdrive.dir = data.dir;
    if (data.gdrive_storage) this.gdrive.storage = data.gdrive_storage;
  }

  // Create and render a Picker object for searching images.
  createPicker() {
    var self = this;
    if (this.gdrive.pickerApiLoaded && this.gdrive.oauthToken) {
      var origin = window.location.protocol + "//" + window.location.host;
      var view = new google.picker.View(google.picker.ViewId.DOCS);
      if (this.gdrive.mimetypes) view.setMimeTypes(this.gdrive.mimetypes);
      var picker = new google.picker.PickerBuilder()
        .enableFeature(google.picker.Feature.MULTISELECT_ENABLED)
        .setOAuthToken(self.gdrive.oauthToken)
        .setCallback(self.pickerCallback.bind(self))
        .setOrigin(origin);

      if (this.gdrive.navbar_hidden)
        picker.enableFeature(google.picker.Feature.NAV_HIDDEN);

      if (this.gdrive.locale) picker.setLocale(this.gdrive.locale);

      picker.addView(view);
      debugger;
      this.rpc("/gdrive_picker_path", {
        res_id: this.props.record.resId,
        res_model: this.props.record.resModel,
        gdrive: this.gdrive,
      }).then(function (data) {
        var drive_path = null;
        if (data.dir_id) {
          drive_path = data.dir_id;
        } else {
          drive_path = self.gdrive.dir;
        }
        if (drive_path) {
          picker.addView(
            new google.picker.DocsView()
              .setParent(drive_path)
              .setLabel("Current Odoo record"),
          );
          picker.addView(
            new google.picker.DocsUploadView()
              .setParent(drive_path)
              .setIncludeFolders(true)
              .setLabel("Upload to current Odoo record"),
          );
        } else {
          picker.addView(
            new google.picker.DocsUploadView().setIncludeFolders(true),
          );
        }
        picker.addView(google.picker.ViewId.DOCUMENTS);
        picker.build().setVisible(true);
      });
    }
  }

  async _downloadFromGdrive(document) {
    var def = $.Deferred();
    let url =
      "https://www.googleapis.com/drive/v2/files/" +
      document.id +
      "?alt=media&source=downloadUrl";
    let headers = {
      headers: { Authorization: "Bearer " + this.gdrive.oauthToken },
    };
    fetch(url, headers).then((response) => {
      response.blob().then((blob) => {
        this.blobsGdrive.push({
          blob: blob,
          name: document.name,
        });
        def.resolve();
      });
    });
    return def;
  }

  _copyToOdooFromGdrive(document) {
    var deferreds = [];
    this.filesGdrive = [];
    this.blobsGdrive = [];
    // DOWNLOADING
    deferreds.push(this._downloadFromGdrive(document));

    // UPLOADING
    Promise.all(deferreds).then((res) => {
      for (var i = 0; i < this.blobsGdrive.length; i++)
        this.filesGdrive.push(
          new File([this.blobsGdrive[i].blob], this.blobsGdrive[i].name),
        );
      this.ondropGdrive(this.filesGdrive);
    });
  }

  _copyURLFromGdrive(document) {
    this.props.update(document.url);
  }

  pickerCallback(data) {
    var self = this;
    var url = "nothing";
    if (data[google.picker.Response.ACTION] == google.picker.Action.PICKED) {
      // var def = $.Deferred();
      // if (this.gdrive.storage == 'any')
      //     this._dialogStorageGdrive(def);
      // else
      //     def.resolve();
      // def.then(res => {
      // SELECT DOCUMENTS
      console.log(data);
      var docs = data[google.picker.Response.DOCUMENTS];
      var documents = [];
      for (var i = 0; i < docs.length; i++) {
        var doc = docs[i];
        documents.push({
          id: doc[google.picker.Document.ID],
          name: doc[google.picker.Document.NAME],
          url:
            doc[google.picker.Document.EMBEDDABLE_URL] ||
            doc[google.picker.Document.URL],
        });

        // if (this.gdrive.storage == 'copy')
        //     this._copyToOdooFromGdrive(doc);

        // if (this.gdrive.storage == 'url')
        this._copyURLFromGdrive(doc);
      }
      // d});
    }
  }

  _setStorageGdrive(value, def) {
    this.gdrive.storage = value;
    def.resolve();
  }

  _dialogStorageGdrive(def) {
    var self = this;
    new Dialog(this, {
      title: _t("Google Drive select storage"),
      size: "medium",
      $content: $("<div>").html(
        _t("<p>Please, select file (files) storage:<p/>"),
      ),
      buttons: [
        {
          text: _t("Google Drive url"),
          classes: "btn-primary",
          close: true,
          click: function () {
            self._setStorageGdrive("url", def);
          },
        },
        {
          text: _t("Odoo copy"),
          classes: "btn-primary",
          close: true,
          click: function () {
            self._setStorageGdrive("copy", def);
          },
        },
        { text: _t("Cancel"), close: true },
      ],
    }).open();
  }

  async _onGoogleDrivePicker(e) {
    var self = this;
    try {
      // wait access token, then open picker
      let script = document.createElement("script");
      let script2 = document.createElement("script");

      script2.onload = async () => {
        this.gdrive.oauthToken = localStorage.getItem("gdrive_oauthToken");
        const expire_at = localStorage.getItem("gdrive_auth2_expires_at") || 0;
        const now = new Date().getTime();
        this.config_read.then((data) => {
          // get new access token
          if (!this.gdrive.oauthToken || now > expire_at) {
            if (this.gdrive.clientId) {
              console.log(now);
              console.log(expire_at);
              // TODO(developer): Replace with your client ID and required scopes
              const tokenClient = google.accounts.oauth2.initTokenClient({
                client_id: this.gdrive.clientId,
                scope: this.gdrive.scope,
                callback: (tokenResponse) => {
                  console.log(tokenResponse);
                  this.gdrive.oauthToken = tokenResponse.access_token;
                  localStorage.setItem(
                    "gdrive_oauthToken",
                    tokenResponse.access_token,
                  );
                  localStorage.setItem(
                    "gdrive_auth2_expires_at",
                    new Date().getTime() + tokenResponse.expires_in,
                  );

                  gapi.load("picker", {
                    callback: () => {
                      this.gdrive.pickerApiLoaded = true;
                      this.createPicker();
                    },
                  });
                },
              });

              if (this.gdrive.oauthToken === null) {
                console.log(this);
                // Prompt the user to select a Google Account and ask for consent to share their data
                // when establishing a new session.
                tokenClient.requestAccessToken({ prompt: "consent" });
              } else {
                // Skip display of account chooser and consent dialog for an existing session.
                tokenClient.requestAccessToken({ prompt: "" });
              }
            } else {
              console.log(
                _t(
                  "Cannot access parameter 'document.gdrive.client.id' check your configuration in General Settings",
                ),
              );
              alert(
                _t(
                  "Cannot access parameter 'document.gdrive.client.id' check your configuration in General Settings",
                ),
              );
            }
          } else {
            // token already exist
            console.log("Token already exist");
          }
        });
      };

      script.src = "https://apis.google.com/js/api.js";
      script2.src = "https://accounts.google.com/gsi/client";
      document.head.appendChild(script);
      document.head.appendChild(script2);
    } catch (err) {
      console.log("Error load Google Drive API", err);
    }
  }

  async ondropGdrive(files) {
    await this.props.record.chatter.fileUploader.uploadFiles(files);
    // await this.fileUploader.uploadFiles(file);
    // await this._fileUploaderRef.comp.uploadFiles(files);
    this.props.record.chatter.refresh();
  }
}

FieldGoogleDrivePicker.template = "FieldGdrive";
FieldGoogleDrivePicker.props = standardFieldProps;

registry.category("fields").add("gdrive_picker_field", FieldGoogleDrivePicker);
