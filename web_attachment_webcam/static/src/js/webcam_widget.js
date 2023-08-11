/*
    Copyright 2016 Siddharth Bhalgami <siddharth.bhalgami@techreceptives.com>
    Copyright 2020 Shurshilov Artem <shurshilov.a@yandex.ru>
    License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
*/
odoo.define("web_attachment_webcam.webcam_widget", function (require) {
  "use strict";

  var core = require("web.core");
  var _t = core._t;
  var QWeb = core.qweb;
  var Dialog = require("web.Dialog");
  var Chatter = require("mail.Chatter");
  var DocumentViewer = require("mail.DocumentViewer");
  var field_utils = require("web.field_utils");
  var AttachmentBox = require("mail.AttachmentBox");

  Chatter.include({
    start: function () {
      var self = this;
      this._super.apply(this, arguments);
      self.webcam_start();
    },

    webcam_start: function () {
      var self = this,
        WebCamDialog = $(QWeb.render("WebCamDialog")),
        img_data;

      Webcam.set({
        width: 320,
        height: 240,
        dest_width: 320,
        dest_height: 240,
        image_format: "jpeg",
        jpeg_quality: 90,
        force_flash: false,
        fps: 45,
        swfURL: "/attachments_manager/static/src/libs/webcam.swf",
        //force_flash: true,
      });

      self.$el.on("click", ".o_form_binary_file_web_cam", function (evt) {
        // Init Webcam
        new Dialog(self, {
          size: "large",
          dialogClass: "o_act_window",
          title: _t("WebCam Booth"),
          $content: WebCamDialog,
          buttons: [
            {
              text: _t("Take Snapshot"),
              classes: "btn-primary take_snap_btn",
              click: function () {
                Webcam.snap(function (data) {
                  img_data = data;
                  // Display Snap besides Live WebCam Preview
                  WebCamDialog.find("#webcam_result").html(
                    '<img src="' + img_data + '"/>',
                  );
                });
                // Remove "disabled" attr from "Save & Close" button
                $(".save_close_btn").removeAttr("disabled");
              },
            },
            {
              text: _t("Save & Close"),
              classes: "btn-primary save_close_btn",
              close: true,
              click: function () {
                if (!img_data) return;
                var img_data_base64 = img_data.split(",")[1];

                /*
                                    Size in base64 is approx 33% overhead the original data size.

                                    Source: -> http://stackoverflow.com/questions/11402329/base64-encoded-image-size
                                            -> http://stackoverflow.com/questions/6793575/estimating-the-size-of-binary-data-encoded-as-a-b64-string-in-python

                                            -> https://en.wikipedia.org/wiki/Base64
                                            [ The ratio of output bytes to input bytes is 4:3 (33% overhead).
                                            Specifically, given an input of n bytes, the output will be "4[n/3]" bytes long in base64,
                                            including padding characters. ]
                                */

                // From the above info, we doing the opposite stuff to find the approx size of Image in bytes.
                var approx_img_size = 3 * (img_data_base64.length / 4); // like... "3[n/4]"

                // Upload image in Binary Field
                self.onwebcam(img_data_base64, "image/jpeg");
                //self.on_file_uploaded(approx_img_size, "web-cam-preview.jpeg", "image/jpeg", img_data_base64);
              },
            },
            {
              text: _t("Close"),
              close: true,
            },
          ],
        }).open();
        Webcam.attach(WebCamDialog.find("#live_webcam")[0]);

        // At time of Init "Save & Close" button is disabled
        $(".save_close_btn").attr("disabled", "disabled");

        // Placeholder Image in the div "webcam_result"
        WebCamDialog.find("#webcam_result").html(
          '<img src="/attachments_manager/static/src/libs/webcam_placeholder.png"/>',
        );
      });
    },

    _openAttachmentBox: function () {
      var def = $.Deferred();
      if (this.fields.attachments) {
        this._closeAttachments();
      }
      this.fields.attachments = new AttachmentBox(
        this,
        this.record,
        this.attachments,
      );
      var $anchor = this.$(".o_chatter_topbar");
      if (this._composer) {
        var $anchor = this.$(".o_thread_composer");
      } else {
        var $anchor = this.$(".o_chatter_topbar");
      }
      this.fields.attachments.insertAfter($anchor).then(function () {
        def.resolve();
      });
      this.$el.addClass("o_chatter_composer_active");
      this.$(".o_chatter_button_attachment").addClass("o_active_attach");

      this._isAttachmentBoxOpen = true;
      return def;
    },

    check_attachment_box: function () {
      console.log("check_attachment_box");
      var def = $.Deferred();

      if (!this._isAttachmentBoxOpen)
        this._openAttachmentBox().then(function () {
          def.resolve();
        });
      else def.resolve();

      return def;
    },

    onwebcam: function (base64, mimetype) {
      var self = this;
      self.check_attachment_box().then(function () {
        function urltoFile(url, filename, mimeType) {
          return fetch(url)
            .then(function (res) {
              return res.arrayBuffer();
            })
            .then(function (buf) {
              return new File([buf], filename, { type: mimeType });
            });
        }

        urltoFile(
          "data:" + mimetype + ";base64," + base64,
          "snapshot.jpg",
          mimetype,
        ).then(function (file) {
          var form_upload = document.querySelector("form.o_form_binary_form");
          if (null === form_upload) {
            return;
          }

          var form_data = new FormData(form_upload);
          form_data.set("ufile", file);

          $.ajax({
            url: form_upload.getAttribute("action"),
            method: form_upload.getAttribute("method"),
            type: form_upload.getAttribute("method"),
            processData: false,
            contentType: false,
            data: form_data,
            success: function (data) {
              self._onReloadAttachmentBox();
            },
            error: function (jqXHR, textStatus, errorThrown) {
              console.error(jqXHR, textStatus, errorThrown);
            },
          });
        });
      });
    },
  });

  Dialog.include({
    destroy: function () {
      // Shut Down the Live Camera Preview | Reset the System
      Webcam.reset();
      this._super.apply(this, arguments);
    },
  });
});
