/** @odoo-module */
import { registerMessagingComponent } from "@mail/utils/messaging_component";
const components = {
  Dialog: require("web.OwlDialog"),
};

const { Component, useState, useRef } = owl;

class AttachmentWebcamDialog extends Component {
  /**
   * @override
   */
  constructor(...args) {
    super(...args);

    this.state = useState({
      snapshot: "/web_attachment_webcam/static/src/img/webcam_placeholder.png",
    });
    // to manually trigger the dialog close event
    this._dialogRef = useRef("dialog");
    this._liveWebcamDiv = useRef("live_webcam");
  }

  // get attachmentUrlNoDownload() {
  //     if (this.attachment.isTemporary) {
  //         return '';
  //     }
  //     return this.env.session.url('/web/content', {
  //         id: this.attachment.id,
  //     });
  // }

  async willStart() {
    let options = {
      width: this.env.session.am_webcam_width
        ? this.env.session.am_webcam_width
        : 320,
      height: this.env.session.am_webcam_height
        ? this.env.session.am_webcam_height
        : 240,
      dest_width: this.env.session.am_webcam_width
        ? this.env.session.am_webcam_width
        : 320,
      dest_height: this.env.session.am_webcam_height
        ? this.env.session.am_webcam_height
        : 240,
      image_format: "jpeg",
      jpeg_quality: 90,
      force_flash: false,
      fps: 45,
      swfURL: "/attachments_manager/static/src/libs/webcam.swf",
    };
    if (this.props.webcamRear)
      options.constraints = {
        video: true,
        facingMode: "environment",
      };
    Webcam.set(options);
  }

  mounted() {
    Webcam.attach(this._liveWebcamDiv.el);
  }

  willUnmount() {
    Webcam.reset();
  }
  //--------------------------------------------------------------------------
  // Public
  //--------------------------------------------------------------------------

  /**
   * @returns {string}
   */
  getBody() {
    return _.str.sprintf(
      this.env._t(
        `You can setting default photo size and quality in general settings`,
      ),
    );
  }

  /**
   * @returns {string}
   */
  getTitle() {
    return this.env._t("Attachments manager Webcam");
  }

  //--------------------------------------------------------------------------
  // Handlers
  //--------------------------------------------------------------------------

  /**
   * @private
   */
  _onClickCancel(ev) {
    ev.stopPropagation();
    ev.preventDefault();
    this._dialogRef.comp._close();
  }

  _onWebcamSnapshot() {
    Webcam.snap((data) => {
      // Display Snap besides Live WebCam Preview
      this.state.snapshot = data;
    });
  }

  async _onWebcamSave(ev) {
    if (!this.state.snapshot) return;
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
    //var approx_img_size = 3 * (img_data_base64.length / 4)  // like... "3[n/4]"

    // Upload image in Binary Field
    await this.onwebcam(this.state.snapshot.split(",")[1], "image/jpeg");
    this._onClickCancel(ev);
  }

  urltoFile(url, filename, mimeType) {
    return fetch(url)
      .then(function (res) {
        return res.arrayBuffer();
      })
      .then(function (buf) {
        return new File([buf], filename, { type: mimeType });
      });
  }

  async onwebcam(base64, mimetype) {
    let file = await this.urltoFile(
      "data:" + mimetype + ";base64," + base64,
      "snapshot.jpg",
      mimetype,
    );
    this.trigger("dialog-file", file);
  }
}

Object.assign(AttachmentWebcamDialog, {
  components,
  template: "web_attachment_webcam.AttachmentWebcamDialog",
});
registerMessagingComponent(AttachmentWebcamDialog);
export default AttachmentWebcamDialog;
