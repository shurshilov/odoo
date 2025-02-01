/** @odoo-module */

import { AttachmentBox } from '@mail/components/attachment_box/attachment_box';
import { patch } from 'web.utils';
import Dialog from 'web.Dialog';
import core from 'web.core';
const _t = core._t;
import { get_cookie, set_cookie } from 'web.utils.cookies';
let accessToken = null;
let pickerInited = false;
let gisInited = false;


patch(AttachmentBox.prototype, 'google_drive_picker/static/src/components/google_drive_picker/google_drive_picker.js', {
    async willStart(...args) {
        await this._super(...args);

        this.config_read = $.Deferred();
        this.cookieName = "gdrive.oauthToken";
        // Scope to use to access user's Drive items.
        this.scope = ['https://www.googleapis.com/auth/drive'];
        this.gdrive = {
            pickerApiLoaded: false,
            oauthToken: false
        };
        this._parseConfig(this.env.session);
        this.config_read.resolve();


        let scriptEle = document.createElement("script");
        scriptEle.setAttribute("type", "text/javascript");
        scriptEle.setAttribute("src", "https://accounts.google.com/gsi/client");
        document.body.appendChild(scriptEle);
        scriptEle.addEventListener("load", () => {
            console.log("File loaded")
            try {
                gapi.load('picker', this.onPickerApiLoad.bind(this));
            }
            catch (err) {
                console.log('Error load Google Drive API', err);
            }
        });

    },

    onPickerApiLoad() {
        pickerInited = true;
        // TODO(developer): Replace with your client ID and required scopes
        this.tokenClient = google.accounts.oauth2.initTokenClient({
            client_id: this.gdrive.clientId,
            scope: 'https://www.googleapis.com/auth/drive.metadata.readonly',
            callback: '', // defined later
        });
        gisInited = true;
    },

    async _onGoogleDrivePicker(e) {
        try {
            // wait access token, then open picker
            accessToken = await this.generate_access_token()
            await this.createPicker();
        }
        catch (err) {
            console.log('Error load Google Drive API', err);
        }
    },

    generate_access_token() {
        const generate_access_token_done = $.Deferred();
        this.tokenClient.callback = async (response) => {
            if (response.error !== undefined) {
                throw (response);
            }
            accessToken = response.access_token;
            generate_access_token_done.resolve(accessToken);
        };

        if (accessToken === null) {
            // Prompt the user to select a Google Account and ask for consent to share their data
            // when establishing a new session.
            this.tokenClient.requestAccessToken({ prompt: 'consent' });
        } else {
            // Skip display of account chooser and consent dialog for an existing session.
            this.tokenClient.requestAccessToken({ prompt: '' });
        }

        return generate_access_token_done
    },

    _parseConfig(data) {
        data = data.gdrive;
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

    saveGdriveTokenCookie(oauthToken, expires_at) {
        set_cookie(this.cookieName, oauthToken);
        set_cookie('gdrive_auth2_expires_at', expires_at);
        return;
    },

    readGdriveTokenCookie() {
        return get_cookie(this.cookieName);
    },

    readGdriveExpiresAt() {
        return get_cookie('gdrive_auth2_expires_at');
    },

    // Create and render a Picker object for searching images.
    createPicker() {
        //debugger
        var self = this;
        if (pickerInited && accessToken) {
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
            this.env.services.rpc({
                //this._rpc({
                route: '/gdrive_picker_path',
                params: {
                    'res_id': this.chatter.thread.id,
                    'res_model': this.chatter.thread.model,
                    // 'res_id': this.currentResID,
                    // 'res_model': this.currentResModel,
                    'gdrive': this.gdrive
                }
            }).then(function (data) {
                var drive_path = null
                if (data.dir_id) {
                    drive_path = data.dir_id
                }
                else {
                    drive_path = self.gdrive.dir
                }
                if (drive_path) {
                    picker.addView(new google.picker.DocsView().setParent(drive_path).setLabel("Current Odoo record"))
                    picker.addView(new google.picker.DocsUploadView().setParent(drive_path).setIncludeFolders(true).setLabel("Upload to current Odoo record"))
                }
                else {
                    picker.addView(new google.picker.DocsUploadView().setIncludeFolders(true));
                }
                picker.addView(google.picker.ViewId.DOCUMENTS);
                picker.build().setVisible(true);
            });
        }
    },

    async _downloadFromGdrive(document) {
        var def = $.Deferred();
        let url = 'https://www.googleapis.com/drive/v2/files/' + document.id + '?alt=media&source=downloadUrl';
        let headers = { headers: { 'Authorization': 'Bearer ' + this.gdrive.oauthToken } };
        fetch(url, headers).then(response => {
            response.blob().then(blob => {
                this.blobsGdrive.push({
                    blob: blob,
                    name: document.name
                });
                def.resolve();
            })
        })
        return def;
    },

    _copyToOdooFromGdrive(document) {
        var deferreds = [];
        this.filesGdrive = [];
        this.blobsGdrive = [];
        // DOWNLOADING
        deferreds.push(this._downloadFromGdrive(document));

        // UPLOADING
        Promise.all(deferreds).then(res => {
            for (var i = 0; i < this.blobsGdrive.length; i++)
                this.filesGdrive.push(new File([this.blobsGdrive[i].blob], this.blobsGdrive[i].name));
            this.ondropGdrive(this.filesGdrive);
        });
    },

    _copyURLFromGdrive(document) {
        this.env.services.rpc({
            model: 'ir.attachment',
            method: 'create',
            args: [{
                'name': document.name,
                'type': 'url',
                //'type': 'gdrive',
                'url': document.url,
                'res_id': this.chatter.thread.id,
                'res_model': this.chatter.thread.model,
                'mimetype': document.mimeType
                //'icon_url': document.iconUrl
            }],
        }).then(res => {
            this.chatter.thread.fetchAttachments.bind(this.chatter.thread)();
            this.chatter.thread.refresh();
        })
    },

    pickerCallback(data) {
        if (data.action === google.picker.Action.PICKED) {
            var def = $.Deferred();
            if (this.gdrive.storage == 'any')
                this._dialogStorageGdrive(def);
            else
                def.resolve();
            def.then(res => {
                // SELECT DOCUMENTS
                console.log(data)
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

    _setStorageGdrive(value, def) {
        this.gdrive.storage = value;
        def.resolve();
    },

    _dialogStorageGdrive(def) {
        var self = this;
        new Dialog(this, {
            title: _t('Google Drive select storage'),
            size: 'medium',
            $content: $('<div>').html(_t('<p>Please, select file (files) storage:<p/>')),
            buttons: [
                { text: _t('Google Drive url'), classes: 'btn-primary', close: true, click: function () { self._setStorageGdrive('url', def) } },
                { text: _t('Odoo copy'), classes: 'btn-primary', close: true, click: function () { self._setStorageGdrive('copy', def) } },
                { text: _t('Cancel'), close: true }]
        }).open()
    },

    async _onGoogleDrivePicker(e) {
        var self = this;
        try {
            // wait access token, then open picker
            var script = document.createElement('script');
            script.onload = async function () {
                //do stuff with the script

                let access_token = await self.generate_access_token()
                gapi.load('picker', {
                    'callback': function() {
                        self.gdrive.pickerApiLoaded = true;
                        // var expire_at = self.readGdriveExpiresAt() || 0;
                        // var now = new Date().getTime();
                        // if (self.gdrive.oauthToken && now <= expire_at)
                            self.createPicker();
                        // auto open picker
                        // else
                        //     alert(_t("Your Access Token expired, please refresh page and authorize again"));
                    }
                });
            };
            script.src = 'https://apis.google.com/js/api.js?onload=onApiLoad';

            document.head.appendChild(script);
        }
        catch(err) {
            console.log('Error load Google Drive API', err);
        }
    },

    async ondropGdrive(files) {
        await this._fileUploaderRef.comp.uploadFiles(files);
        this.chatter.thread.refresh();
    }
});

