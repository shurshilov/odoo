/** @odoo-module **/
import { ImageField } from "@web/views/fields/image/image_field";
import { patch } from "web.utils";
import { Dialog } from "@web/core/dialog/dialog";
import { Component, xml } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

class ImageDialog extends Component {}
ImageDialog.template = xml`
<Dialog title="props.tittle" size="'xl'">
    <t t-if="props.url">
        <div style="display: flex;text-align: center;justify-content: center;align-items: center;">
            <img
            class="img img-fluid"
            alt="Binary file"
            t-att-src="props.url"/>
        </div>
    </t>
</Dialog>`;
ImageDialog.components = { Dialog };

patch(ImageField.prototype, "field_image_preview", {
  async setup() {
    this._super(...arguments);
    this.dialogService = useService("dialog");
  },

  fieldImagePreview: function () {
    const name_field = this.props.name;
    if (
      name_field == "image_1024" ||
      name_field == "image_256" ||
      name_field == "image_512" ||
      name_field == "image_128"
    )
      name_field = "image_1920";

    this.dialogService.add(ImageDialog, {
      tittle: this.props.name,
      url: this.getUrl(this.props.name),
    });
  },
});
