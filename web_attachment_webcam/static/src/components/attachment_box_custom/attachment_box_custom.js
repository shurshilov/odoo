/** @odoo-module */
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

import { AttachmentBox } from "@mail/components/attachment_box/attachment_box";
import AttachmentWebcamDialog from "@web_attachment_webcam/components/attachment_webcam/attachment_webcam";
import Dialog from "web.Dialog";
import { patch } from "web.utils";
const { useState, useRef } = owl;
import { registerPatch } from "@mail/model/model_core";

patch(AttachmentBox.prototype, "web_attachment_webcam", {
  async willStart(...args) {
    this._super(...args);
    this.state = useState({
      hasFavoritesDialog: false,
      hasWebcamDialog: false,
      snapshot: "",
      attachments_favorite: [],
    });
    this._amNewRef = useRef("am-new");
  },

  willUnmount(...args) {
    this._super(...args);
    $(this.el).contextMenu("destroy");
  },

  mounted(...args) {
    var self = this;
    // make button open the menu
    this._amNewRef.el.addEventListener("click", (e) => {
      e.preventDefault();
      $(this._amNewRef.el).contextMenu();
    });

    $(this.el).contextMenu({
      selector: ".oe_button_control_new",
      build: function ($trigger, e) {
        // this callback is executed every time the menu is to be shown
        // its results are destroyed every time the menu is hidden
        // e is the original contextmenu event, containing e.pageX and e.pageY (amongst other data)
        return {
          callback: function (key, options) {
            e.target = e.currentTarget;
            var odoo_callback = self[key].bind(self);
            odoo_callback(e);
          },
          items: {
            _openFrontCamera: {
              name: "Camera front",
              icon: "fa-mobile-phone",
              disabled: function () {
                return false;
              },
            },
            _openRearCamera: {
              name: "Camera rear",
              icon: "fa-camera",
              disabled: function () {
                return false;
              },
            },
          },
        };
      },
    });
  },

  _openRearCamera(ev) {
    this.webcamRear = true;
    this.state.hasWebcamDialog = true;
  },

  _openFrontCamera(ev) {
    this.state.hasWebcamDialog = true;
  },

  _onWebcamClosed() {
    this.state.hasWebcamDialog = false;
    this.webcamRear = false;
  },

  _onWebcamCallback(ev) {
    // TO DO refresh
    // updating temp attachment or iverride fileuploader _createTemporaryAttachments func
    this.fileUploader.uploadFiles([ev.detail]);
    // this._fileUploaderRef.comp.uploadFiles([ev.detail]);
  },
});

Object.assign(AttachmentBox, {
  components: {
    Dialog: Dialog,
    AttachmentWebcamDialog: AttachmentWebcamDialog,
  },
});

return AttachmentBox;
