/** @odoo-module */

import { registry } from "@web/core/registry";
import {
  Many2OneField,
  many2OneField,
} from "@web/views/fields/many2one/many2one_field";

export class AttachmentMany2OneAudioWidget extends Many2OneField {
  setup() {
    super.setup();
  }
  get url() {
    console.log(this.resId, "this.resId ");
    return "/web/content/" + this.resId + "?download=true";
  }
}
AttachmentMany2OneAudioWidget.template =
  "attachments_widgets.AudioMany2OneField";

export const attachmentMany2OneAudioWidget = {
  ...many2OneField,
  component: AttachmentMany2OneAudioWidget,
};
registry
  .category("fields")
  .add("attachment_many2one_audio_widget", attachmentMany2OneAudioWidget);
