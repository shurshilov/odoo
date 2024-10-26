/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";
import { Dialog } from "@web/core/dialog/dialog";
import { Chatter } from "@mail/core/web/chatter";
import { _t } from "@web/core/l10n/translation";
import { Component, xml, useState } from "@odoo/owl";

class SynologyTreeDialog extends Component {
  async setup() {
    this.rpc = useService("rpc");
    this.state = useState({
      files: [],
      loading: true,
    });
    console.log(this.props);
    await this._onSynologyTree(false, this.props.event);
  }

  async _onSynologyDownload(ev) {
    ev.stopPropagation();
    ev.preventDefault();
    let path = $(ev.target).data("path");
    let res = await this.rpc("/web/dataset/call_kw", {
      model: "ir.attachment",
      method: "synology_download",
      kwargs: {
        // path: path,
      },
      args: [path],
    });
    window.location.href = res;
  }

  async _onSynologyRequest(funcAPT = "get_info", params_list = []) {
    console.log("params_list", params_list);
    let res = await this.rpc(
      "/web/dataset/call_kw",
      {
        model: "ir.attachment",
        method: "synology",
        kwargs: {
          funcAPI: funcAPT,
          params_list: params_list,
        },
        args: [],
      },
      { silent: true },
    );

    return res;
  }

  async _onSynologyImport(ev) {
    ev.stopPropagation();
    ev.preventDefault();
    let path = $(ev.target).data("path");
    console.log("import_path", path);
    let res = await this.rpc("/web/dataset/call_kw", {
      model: "ir.attachment",
      method: "synology_import",
      kwargs: {
        path: path,
        res_model: this.props.chatter.props.threadModel,
        res_id: this.props.chatter.props.threadId,
      },
      args: [],
    });
    // this.props.chatter.refresh();
    this.props.chatter.load(this.props.chatter.state.thread, [
      "followers",
      "attachments",
      "suggestedRecipients",
    ]);
    return res;
  }

  _onAttachmentDownload(ev) {
    ev.stopPropagation();
    ev.preventDefault();
    this._onDownloadAttachment(ev);
  }

  _onDownloadAttachment(ev) {
    ev.stopPropagation();
    ev.preventDefault();
    var activeAttachmentID = $(ev.currentTarget).data("id");
    var attachmentObject = {};
    _.each(this.props.chatter.attachments, function (attachment) {
      if (attachment.id === activeAttachmentID) {
        attachmentObject = attachment;
        return;
      }
    });

    // if synology file
    if (
      attachmentObject.weburl &&
      attachmentObject.weburl.indexOf("SYNO.FileStation.Download") != -1
    ) {
      //window.open(, '_blank');
      window.location.href =
        attachmentObject.weburl.replace("mode=open", "mode=download") +
        session.synology_sid;
      return;
    }

    window.location.href = attachmentObject.url;
    //this._super.apply(this, arguments);
  }

  async _onSynologyTree(mode, ev, path = undefined) {
    ev.stopPropagation();
    ev.preventDefault();

    // let path = $(ev.currentTarget).data("path");
    // let path = event.currentTarget.getAttribute("data-path");
    console.log("path", path);
    if (mode == "back") {
      let lastIndex = this.state.files[0].path.lastIndexOf("/");
      path = this.state.files[0].path.slice(0, lastIndex);
      lastIndex = path.lastIndexOf("/");
      path = path.slice(0, lastIndex);
    }
    // this.SynologyTree.find(`img[data-path='${path}']`).show();
    console.log(path);

    if (!path) {
      this.res = await this._onSynologyRequest("get_list_share");
      this.state.files = this.res.data.shares;
      this.state.loadig = true;
    } else {
      // const nodeTree = this.SynologyTree.find(`div[data-path='${path}']`);
      // // check opened
      // const opened = nodeTree.children().eq(1).hasClass("fa-folder-open");
      // // save
      // const old =
      //   nodeTree.children().eq(0)[0].outerHTML +
      //   nodeTree.children().eq(1)[0].outerHTML +
      //   nodeTree.children().eq(2)[0].outerHTML;
      // if (opened) nodeTree.html(old);
      // else {
      this.res = await this._onSynologyRequest("get_file_list", [path]);
      this.state.files = this.res.data.files;
      // const nextTree = $(qweb.render("SynologyTree", { files: this.files }));
      // nodeTree.html(old + nextTree[0].outerHTML);
      // }
      // toogle folder
      // nodeTree.children().eq(1).toggleClass("fa-folder");
      // nodeTree.children().eq(1).toggleClass("fa-folder-open");
    }

    // this.popup_preview.$el.html(this.SynologyTree);

    // this.SynologyTree.find(`img[data-path='${path}']`).hide();

    // // добавляем действия, если первый раз то на все основе дерево
    // // иначе только на поддеревья
    // const treeAddActions = this.SynologyTree;

    // treeAddActions
    //   .find(".folder")
    //   .on("click", this._onSynologyTree.bind(this, "forward"));
    // treeAddActions
    //   .find(".file")
    //   .on("click", this._onSynologyTree.bind(this, "forward"));
    // treeAddActions
    //   .find(".oe_button_import_from_synology")
    //   .on("click", this._onSynologyImport.bind(this));
    // treeAddActions
    //   .find(".oe_button_download_from_synology")
    //   .on("click", this._onSynologyDownload.bind(this));
    // treeAddActions
    //   .find(".oe_button_back")
    //   .on("click", this._onSynologyTree.bind(this, "back"));
  }
}

SynologyTreeDialog.template = xml`
<Dialog title="props.tittle" size="'xl'">
    <div t-name="SynologyTree" class="SynologyTree" style="padding:10px;">
        <div class="col-xs-12 col-12 o_form_view ">
            <t t-if="back">
                <div>
                    <button t-on-click="(ev) => this._onSynologyTree('back', ev)"
                    class='btn btn-link btn-sm oe_button_back' title="Back" type="button">
                        <i class="fa fa-backward"/>
 Back
                    </button>
                </div>
            </t>
            <t t-if="state.loading">
                <img style="align-self: center;width:25px;height:25px" id="synology-loading" src="/synology_drive_picker/static/description/loading.gif"/>
            </t>
            <t t-foreach="state.files" t-as="file" t-key="file.path">
                <t t-if="file.isdir">
                    <div t-on-click="(ev) => this._onSynologyTree('forward', ev, file.path)"
                    t-attf-data-path="{{file.path}}" class="col-xs-12 folder" style="margin-left: 30px;border-left: 1px solid #bbbbbb;padding-left: 10px;">
                        <img t-attf-data-path="{{file.path}}" style="display:none;align-self: center;width:15px;height:15px" src="/synology_drive_picker/static/description/loading.gif"/>
                        <i class="fa fa-folder" style="padding-right: 5px;cursor:pointer;"/>
                        <span>
                            <t t-esc="file.name"/>
                        </span>
                    </div>
                </t>
                <t t-else="">
                    <div t-on-click="(ev) => this._onSynologyTree('forward', ev)"
                    t-attf-data-path="{{file.path}}" class="col-xs-12 file" style="margin-left: 30px;border-left: 1px solid #bbbbbb;padding-left: 10px;">
                        <t t-esc="file.name"/>
                        <button t-on-click="(ev) => this._onSynologyDownload(ev)"
                        t-attf-data-path="{{file.path}}" class='btn btn-link btn-sm oe_button_download_from_synology' title="Download to device" type="button">
                            <i class="fa fa-download"/>
 Download
                        </button>
                        <button t-on-click="(ev) => this._onSynologyImport(ev)"
                        t-attf-data-path="{{file.path}}" class='btn btn-link btn-sm oe_button_import_from_synology' title="Download to Odoo" type="button">
                            <i class="fa fa-cloud-download"/>
 Import Odoo
                        </button>
                    </div>
                </t>

            </t>
        </div>
    </div>
</Dialog>`;
SynologyTreeDialog.components = { Dialog };

patch(Chatter.prototype, {
  setup() {
    super.setup();
    this.rpc = useService("rpc");
  },

  // _onAttachmentView: function (ev) {
  //   ev.stopPropagation();
  //   ev.preventDefault();
  //   var activeAttachmentID = $(ev.currentTarget).data("id");
  //   var attachmentObject = {};
  //   _.each(this.attachmentIDs, function (attachment) {
  //     if (attachment.id === activeAttachmentID) {
  //       attachmentObject = attachment;
  //       return;
  //     }
  //   });

  //   // if synology file
  //   if (
  //     attachmentObject.weburl &&
  //     attachmentObject.weburl.indexOf("SYNO.FileStation.Download") != -1
  //   ) {
  //     window.open(attachmentObject.weburl + session.synology_sid, "_blank");
  //     return;
  //   }

  //   this._super.apply(this, arguments);
  // },

  _onSynologyDrivePicker: function (ev) {
    ev.stopPropagation();
    ev.preventDefault();
    console.log("chatter", this);
    this.dialogService.add(SynologyTreeDialog, {
      tittle: "Synology tree dialog",
      event: ev,
      chatter: this,
    });
  },
});
