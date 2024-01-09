/** @odoo-module */

import { ChatterTopbar } from "@mail/components/chatter_topbar/chatter_topbar";
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";
import Dialog from "web.Dialog";
import { qweb, _t } from "web.core";

patch(ChatterTopbar.prototype, "synology_drive_picker", {
  setup() {
    this._super(...arguments);
    this.rpc = useService("rpc");
  },
  _onSynologyRequest: async function (funcAPT = "get_info", params_list = []) {
    console.log("params_list", params_list);
    // const action = await this.messaging.rpc({
    //   model: "ir.attachment",
    //   method: "synology",
    //   args: [
    //     {
    //       funcAPI: funcAPT,
    //       params_list: params_list,
    //     },
    //   ],
    // });
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
  },

  _onSynologyImport: async function (ev) {
    ev.stopPropagation();
    ev.preventDefault();
    let path = $(ev.target).data("path");
    console.log("import_path", path);
    let res = await this.rpc("/web/dataset/call_kw", {
      model: "ir.attachment",
      method: "synology_import",
      kwargs: {
        path: path,
        res_model: this.props.record.chatter.threadModel,
        res_id: this.props.record.chatter.threadId,
      },
      args: [],
    });
    this.props.record.chatter.refresh();
    return res;
    // this.env.services
    //   .rpc({
    //     model: "ir.attachment",
    //     method: "synology_import",
    //     kwargs: {
    //       path: path,
    //       res_model: this.getParent().context.default_model,
    //       res_id: this.getParent().context.default_res_id,
    //     },
    //   })
    //   .then((res) => {
    //     this.trigger_up("reload_attachment_box");
    //   });
  },

  _onAttachmentDownload: function (ev) {
    ev.stopPropagation();
    ev.preventDefault();
    this._onDownloadAttachment(ev);
  },

  _onDownloadAttachment: function (ev) {
    ev.stopPropagation();
    ev.preventDefault();
    var activeAttachmentID = $(ev.currentTarget).data("id");
    var attachmentObject = {};
    _.each(this.attachmentIDs, function (attachment) {
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
  },

  _onAttachmentView: function (ev) {
    ev.stopPropagation();
    ev.preventDefault();
    var activeAttachmentID = $(ev.currentTarget).data("id");
    var attachmentObject = {};
    _.each(this.attachmentIDs, function (attachment) {
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
      window.open(attachmentObject.weburl + session.synology_sid, "_blank");
      return;
    }

    this._super.apply(this, arguments);
  },

  _onSynologyDownload: async function (ev) {
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

    // this.env.services
    //   .rpc({
    //     model: "ir.attachment",
    //     method: "synology_download",
    //     kwargs: {
    //       path: path,
    //     },
    //   })
    //   .then((url) => {
    //     window.location.href = url;
    //     //window.open(url, '_blank');
    //   });
  },

  _onSynologyDrivePicker: function (ev) {
    ev.stopPropagation();
    ev.preventDefault();
    this.SynologyTree = $(
      qweb.render("SynologyTree", { files: [], loading: true }),
    );
    this.popup_preview = new Dialog(this, {
      size: "large",
      dialogClass: "o_act_window",
      title: _t("Attachments synology picker"),
      $content: this.SynologyTree,
      buttons: [
        {
          text: _t("Close"),
          close: true,
        },
      ],
    }).open();
    this._onSynologyTree(false, ev);
  },

  _onSynologyTree: async function (mode, ev) {
    ev.stopPropagation();
    ev.preventDefault();

    let path = $(ev.currentTarget).data("path");
    if (mode == "back") {
      let lastIndex = this.files[0].path.lastIndexOf("/");
      path = this.files[0].path.slice(0, lastIndex);
      lastIndex = path.lastIndexOf("/");
      path = path.slice(0, lastIndex);
    }
    this.SynologyTree.find(`img[data-path='${path}']`).show();
    console.log(path);

    if (!path) {
      this.res = await this._onSynologyRequest("get_list_share");
      this.files = this.res.data.shares;
      this.SynologyTree = $(
        qweb.render("SynologyTree", { files: this.files, loadig: true }),
      );
    } else {
      const nodeTree = this.SynologyTree.find(`div[data-path='${path}']`);
      // check opened
      const opened = nodeTree.children().eq(1).hasClass("fa-folder-open");
      // save
      const old =
        nodeTree.children().eq(0)[0].outerHTML +
        nodeTree.children().eq(1)[0].outerHTML +
        nodeTree.children().eq(2)[0].outerHTML;
      if (opened) nodeTree.html(old);
      else {
        this.res = await this._onSynologyRequest("get_file_list", [path]);
        this.files = this.res.data.files;
        const nextTree = $(qweb.render("SynologyTree", { files: this.files }));
        nodeTree.html(old + nextTree[0].outerHTML);
      }
      // toogle folder
      nodeTree.children().eq(1).toggleClass("fa-folder");
      nodeTree.children().eq(1).toggleClass("fa-folder-open");
    }
    this.popup_preview.$el.html(this.SynologyTree);

    this.SynologyTree.find(`img[data-path='${path}']`).hide();

    // добавляем действия, если первый раз то на все основе дерево
    // иначе только на поддеревья
    const treeAddActions = this.SynologyTree;
    // this.SynologyTree.find(".folder").off(
    //   "click",
    //   this._onSynologyTree.bind(this, "forward"),
    // );
    // this.SynologyTree.find(".file").off(
    //   "click",
    //   this._onSynologyTree.bind(this, "forward"),
    // );
    // this.SynologyTree.find(".oe_button_import_from_synology").off(
    //   "click",
    //   this._onSynologyImport.bind(this),
    // );
    // this.SynologyTree.find(".oe_button_download_from_synology").off(
    //   "click",
    //   this._onSynologyDownload.bind(this),
    // );
    // this.SynologyTree.find(".oe_button_back").off(
    //   "click",
    //   this._onSynologyTree.bind(this, "back"),
    // );

    treeAddActions
      .find(".folder")
      .on("click", this._onSynologyTree.bind(this, "forward"));
    treeAddActions
      .find(".file")
      .on("click", this._onSynologyTree.bind(this, "forward"));
    treeAddActions
      .find(".oe_button_import_from_synology")
      .on("click", this._onSynologyImport.bind(this));
    treeAddActions
      .find(".oe_button_download_from_synology")
      .on("click", this._onSynologyDownload.bind(this));
    treeAddActions
      .find(".oe_button_back")
      .on("click", this._onSynologyTree.bind(this, "back"));
  },
});
