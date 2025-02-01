/** @odoo-module */

import { AttachmentCard } from "@mail/components/attachment_card/attachment_card";
import { patch } from "web.utils";

patch(AttachmentCard.prototype, "web_attachment_google_drive", {
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
