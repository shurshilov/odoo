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

odoo.define("mail_remote_desktop", function (require) {
  "use strict";

  const components = {
    composer: require("mail/static/src/components/composer/composer.js"),
  };
  const { patch } = require("web.utils");

  var core = require("web.core");
  var qweb = core.qweb;
  var _t = core._t;
  var Dialog = require("web.Dialog");
  var rpc = require("web.rpc");

  /*    var Chatter = require('mail.Chatter');
    var Discuss = require('mail.Discuss');*/

  var JitsiDialog = Dialog.extend({
    dialog_title: _t("Remote desktop"),
    template: "JitsiDialog",

    init: function (parent, parentID) {
      this.parentID = parentID;
      this.jitsi_room = "Eurodoo" + parentID;
      this.parent = parent;

      this._super(parent, {
        title: _t("Remote desktop"),
        size: "large",
        buttons: [
          {
            text: _t("Close"),
            close: true,
            classes: "btn-primary",
            click: this.destroy.bind(this),
          },
        ],
      });
    },

    start: function () {
      var self = this;
      rpc
        .query({
          route: "/domain/voip",
        })
        .then((data) => {
          console.log("DATA DOMAIN");
          console.log(data.domain);
          if (data.domain) this.domain = data.domain;
          else this.domain = "jitsi.ufanet.ru";

          this.$input = this.$("#jitsi");
          this.options = {
            roomName: this.jitsi_room,
            width: "100%",
            height: "100%",
            parentNode: this.$input[0],
          };
          this.api = new JitsiMeetExternalAPI(this.domain, this.options);

          var message = {
            jitsi_room: this.jitsi_room,
            subtype_id: false,
            message_type: "comment",
            content: `https://${this.domain}/${this.jitsi_room}`,
          };

          //this.parent._onPostMessage(message);
          //this.parent.composer._textareaRef.el.value = message;
          this.parent.composer.insertIntoTextInput(message.content);
          this.parent.composer.postMessage();
        });
      return this._super.apply(this, arguments);
    },

    destroy: function () {
      this.api.dispose();
      this._super.apply(this, arguments);
    },
  });

  patch(components.composer, "mail_remote_desktop", {
    _onClickCreateJitsiMeeting() {
      //console.log(this)
      //new JitsiDialog(this, this._defaultThreadID.toString()).open();
      let jitsiDialogNew = new JitsiDialog(
        this,
        this.props.composerLocalId.toString(),
      ).open();
    },
  });

  /*    Discuss.include({
        events: _.extend({}, Discuss.prototype.events, {
            'click .remote-desktop': '_onOpenRemoteDesktop',
        }),

        _onOpenRemoteDesktop: function (ev) {
            new JitsiDialog(this, this._defaultThreadID.toString()).open();
        },
    })*/
});
