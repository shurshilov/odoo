/** @odoo-module */

import { registry } from "@web/core/registry";
import { Many2OneField } from "@web/views/fields/many2one/many2one_field";

export class AttachmentMany2OneAudioWidget extends Many2OneField {
  constructor(...args) {
    super(...args);
  }

  get url() {
    return "/web/content/" + this.resId + "?download=true";
  }

  // _computeIsAudio(extension) {
  //     const audioExtensions = [
  //         'wav',
  //         'ogg',
  //         'mp3',
  //         'mp4',
  //         'oga',
  //         'ogx',
  //         'mpeg'
  //     ];
  //     return audioExtensions.includes(extension);
  // }

  // _computeExtension(filename) {
  //     const extension = filename && filename.split('.').pop();
  //     if (extension) {
  //         return extension;
  //     }
  //     return clear();
  // }

  // _renderReadonly() {
  //     this._super.apply(this, arguments);
  //         if (this.m2o_value) {
  //             const url = this._getUrl(this.m2o_value);

  //             let audio = $('<audio>', {
  //                 'src': url,
  //                 'controls': true,
  //                 'preload': "metadata",
  //             })

  //             // this.$el.append(audio);
  //             this.$el = audio;

  //             audio.on("error", () => {
  //                 this.displayNotification({
  //                     title: _t('Wrong Extension Audio File'),
  //                     message: _t("Format should be in wav, ogg, mp3, mp4, oga, ogx, mpeg"),
  //                     type: 'danger',
  //                 });
  //             })
  //         }
  // }

  // _onInputClick (ev) {
  //     this._super.apply(this, arguments);

  //     let files = ev.target.files;

  //     if (!files || files.length === 0)
  //         return;

  //     const filename = files[0].name;
  //     const extension = this._computeExtension(filename);

  //     if (!this._computeIsAudio(extension))
  //         this.displayNotification({
  //             title: _t('Wrong Extension Audio File'),
  //             message: _t("Format should be in wav, ogg, mp3, mp4, oga, ogx, mpeg"),
  //             type: 'danger',
  //         });
  // }
}
AttachmentMany2OneAudioWidget.template =
  "attachments_widgets.AudioMany2OneField";

registry
  .category("fields")
  .add("attachment_many2one_audio_widget", AttachmentMany2OneAudioWidget);
