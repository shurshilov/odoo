/**
Copyright (C) 2021 Artem Shurshilov <shurshilov.a@yandex.ru>
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
odoo.define("web_attachment_google_drive", function (require) {
  "use strict";

  const components = {
    Attachment: require("mail/static/src/components/attachment/attachment.js"),
  };
  const { patch } = require("web.utils");
  const { Component, useState } = owl;
  const { useRef } = owl.hooks;

  patch(components.Attachment, "web_attachment_google_drive", {
    async _onExportGdrive(ev) {
      if (this.attachment.type === "url") {
        alert("Url attachment cant be uploaded!");
        return;
      }
      // Attachment -> AttachmentList -> AttachmentBox -> generate_access_token
      // wait access token generate
      // TODO: export in discuss
      if (this.__owl__.parent && this.__owl__.parent.__owl__.parent) {
        let access_token =
          await this.__owl__.parent.__owl__.parent.generate_access_token();

        this.env.services
          .rpc({
            route: "/upload_gdrive_file",
            params: {
              attachment_id: this.attachment.id,
              access_token: access_token,
            },
          })
          .then((data) => {
            if (data) {
              this.attachment.originThread.refresh();
              //alert('SUCCESS IMPORT!')
            }
          });
      }
    },
  });
});
