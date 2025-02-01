/** @odoo-module */
const { Component, useRef } = owl;
import { Dialog } from "@web/core/dialog/dialog";
import { _t } from "@web/core/l10n/translation";

class SelectStorageDialog extends Component {
  async setup() {
    super.setup();
    this.saveButton = useRef("saveButton");
  }

  Deferred() {
    let res,
      rej,
      p = new Promise((a, b) => ((res = a), (rej = b)));
    p.resolve = res;
    p.reject = rej;
    return p;
  }

  getText() {
    return _t(`Please, select file (files) storage:`);
  }

  _onConfirmUrl() {
    this.props.confirmUrl();
  }

  _onConfirmBinary() {
    this.props.confirmBinary();
  }
  _onClickCancel(ev) {
    ev.stopPropagation();
    ev.preventDefault();
    this.props.close();
  }
}

SelectStorageDialog.props = {
  close: Function,
  confirmUrl: Function,
  confirmBinary: Function,
};

SelectStorageDialog.components = {
  Dialog,
};

SelectStorageDialog.template = "google_drive_picker.SelectStorage";

export default SelectStorageDialog;
