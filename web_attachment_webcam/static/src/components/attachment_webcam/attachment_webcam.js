/** @odoo-module */
const { Component, useRef, useState, onWillUnmount } = owl;
import { Dialog } from "@web/core/dialog/dialog";
import { session } from "@web/session";

class AttachmentWebcamDialog extends Component {
  //   setup() {
  //     super.setup();
  //     console.log(1)
  //     onWillUnmount(() => this._willUnmount());
  // }
  async setup() {
    super.setup();
    console.log(2);
    this.state = useState({
      snapshot: "",
    });
    onWillUnmount(() => this._willUnmount());
    this.video = useRef("video");
    this.saveButton = useRef("saveButton");
    this.selectCamera = useRef("selectCamera");
    await this.initSelectCamera();
    await this.startVideo();
  }

  _willUnmount() {
    this.stopVideo();
  }

  async initSelectCamera() {
    // добавляем все доступные камеры в селекшен
    const devices = await navigator.mediaDevices.enumerateDevices();
    const videoDevices = devices.filter(
      (device) => device.kind === "videoinput",
    );
    videoDevices.map((videoDevice) => {
      let opt = document.createElement("option");
      opt.value = videoDevice.deviceId;
      opt.innerHTML = videoDevice.label;
      this.selectCamera.el.append(opt);
      return opt;
    });
  }

  onChangeDevice(e) {
    // добавляем обработчик смены камеры
    const device = $(e.target).val();
    this.stopVideo();
    this.startVideo(device);
  }

  takeSnapshot(video) {
    const canvas = document.createElement("canvas");
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const canvasContext = canvas.getContext("2d");
    canvasContext.drawImage(video, 0, 0);
    return canvas.toDataURL("image/jpeg");
  }

  async handleStream(stream) {
    const def = $.Deferred();

    // устанавливаем выбранную камеру в селекшене
    if (stream && stream.getVideoTracks().length)
      this.selectCamera.el.value = stream
        .getVideoTracks()[0]
        .getSettings().deviceId;

    // отображаем видео в диалоге
    this.video.el.srcObject = stream;

    this.video.el.addEventListener("canplay", () => {
      this.video.el.play();
    });

    this.video.el.addEventListener(
      "loadedmetadata",
      () => {
        this.streamStarted = true;
        def.resolve();
      },
      false,
    );

    return def;
  }

  async startVideo(device = null) {
    try {
      let config = {
        width: {
          min: 640,
          ideal: session.am_webcam_width ? session.am_webcam_width : 1280,
        },
        height: {
          min: 480,
          ideal: session.am_webcam_height ? session.am_webcam_height : 720,
        },
        facingMode: this.props.mode ? "user" : "environment",
      };
      if (device) config.deviceId = { exact: device };

      const videoStream = await navigator.mediaDevices.getUserMedia({
        video: config,
      });
      await this.handleStream(videoStream);
    } catch (e) {
      console.error("*** getUserMedia", e);
    } finally {
    }
  }

  stopVideo() {
    // останавливае видео поток
    this.streamStarted = false;
    this.video.el.srcObject.getTracks().forEach((track) => {
      track.stop();
    });
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
    const file = await this.urltoFile(
      "data:" + mimetype + ";base64," + base64,
      "snapshot.jpg",
      mimetype,
    );
    await this.props.onWebcamCallback(file);
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
    this.stopVideo();
    this.props.close();
  }

  _onWebcamSnapshot() {
    this.state.snapshot = this.takeSnapshot(this.video.el);
  }

  async _onWebcamSave(ev) {
    if (!this.state.snapshot) return;

    await this.onwebcam(this.state.snapshot.split(",")[1], "image/jpeg");
    this._onClickCancel(ev);
  }
}

AttachmentWebcamDialog.props = {
  mode: { type: Boolean, optional: true },
  onWebcamCallback: { type: Function, optional: true },
  close: Function,
};

AttachmentWebcamDialog.components = {
  Dialog,
};

AttachmentWebcamDialog.defaultProps = {
  mode: false,
  onWebcamCallback: () => {},
};

AttachmentWebcamDialog.template =
  "web_attachment_webcam.AttachmentWebcamDialog";
export default AttachmentWebcamDialog;
