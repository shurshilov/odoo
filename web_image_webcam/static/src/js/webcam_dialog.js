/** @odoo-module */
const { Component, useRef, useState, onMounted } = owl;
import { Dialog } from "@web/core/dialog/dialog";
import { session } from "@web/session";

class WebcamDialog extends Component {
  async setup() {
    super.setup();
    this.state = useState({
      snapshot: "",
    });
    this.video = useRef("video");
    this.saveButton = useRef("saveButton");
    this.selectCamera = useRef("selectCamera");
    onMounted(() => this._mounted());
  }

  async _mounted() {
    await this.initSelectCamera();
    await this.startVideo();
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
    const device = e.target.value;
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

  Deferred() {
    let res,
      rej,
      p = new Promise((a, b) => ((res = a), (rej = b)));
    p.resolve = res;
    p.reject = rej;
    return p;
  }

  async handleStream(stream) {
    const def = this.Deferred();

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
        width: { ideal: session.am_webcam_width || 1280 },
        height: { ideal: session.am_webcam_height || 720 },
        // facingMode: this.props.mode ? 'user' : 'environment',
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

    // если захват видео из предыдущего устройства был успешным, остановить его
    if (this.video.el.srcObject)
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
    await this.props.onWebcamCallback(base64);
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

WebcamDialog.props = {
  mode: { type: Boolean, optional: true },
  onWebcamCallback: { type: Function, optional: true },
  close: Function,
};

WebcamDialog.components = {
  Dialog,
};

WebcamDialog.defaultProps = {
  mode: false,
  onWebcamCallback: () => {},
};

WebcamDialog.template = "web_image_webcam.WebcamDialog";

export default WebcamDialog;
