/** @odoo-module */

import { ChatterTopbar } from '@mail/components/chatter_topbar/chatter_topbar';
import { patch } from 'web.utils';
import Dialog from 'web.Dialog';
import core from 'web.core';
const _t = core._t;
import { session } from '@web/session';

patch(ChatterTopbar.prototype, 'synology_picker', {
    _onSynologyRequest (funcAPT='get_info', params_list=[]) {
        console.log('params_list', params_list)
        return this.env.services.rpc({
                model: 'ir.attachment',
                method: 'synology',
                kwargs: {
                    funcAPI: funcAPT,
                    params_list: params_list,
                },
            })
    },
    _onSynologyDrivePicker (ev) {
        ev.stopPropagation();
        ev.preventDefault();
        this._onSynologyTree(false, ev);
    },

    _onSynologyImport (ev) {
        ev.stopPropagation();
        ev.preventDefault();
        let path = $(ev.target).data('path');
        console.log('import_path', path)
        this.env.services.rpc({
                model: 'ir.attachment',
                method: 'synology_import',
                kwargs: {
                    path: path,
                    res_model: this.getParent().context.default_model,
                    res_id: this.getParent().context.default_res_id,

                },
        }).then( res =>{
            this.trigger_up('reload_attachment_box');
        });
        
    },

    _onAttachmentDownload (ev) {
        ev.stopPropagation();
        ev.preventDefault();
        this._onDownloadAttachment(ev);
    },

    _onDownloadAttachment (ev) {
        ev.stopPropagation();
        ev.preventDefault();
        var activeAttachmentID = $(ev.currentTarget).data('id');
        var attachmentObject = {};
        _.each(this.attachmentIDs, function (attachment) {
            if (attachment.id === activeAttachmentID){
                attachmentObject = attachment;
                return
            }
        });

        // if synology file
        if (attachmentObject.weburl && attachmentObject.weburl.indexOf('SYNO.FileStation.Download') != -1 ){
            //window.open(, '_blank');
            window.location.href = attachmentObject.weburl.replace('mode=open','mode=download') + session.synology_sid;
            return;
        }
        
        window.location.href = attachmentObject.url;
        //this._super.apply(this, arguments);
    },

    _onAttachmentView (ev) {
        ev.stopPropagation();
        ev.preventDefault();
        var activeAttachmentID = $(ev.currentTarget).data('id');
        var attachmentObject = {};
        _.each(this.attachmentIDs, function (attachment) {
            if (attachment.id === activeAttachmentID){
                attachmentObject = attachment;
                return
            }
        });

        // if synology file
        if (attachmentObject.weburl && attachmentObject.weburl.indexOf('SYNO.FileStation.Download') != -1 ){
            window.open(attachmentObject.weburl + session.synology_sid, '_blank');
            return;
        }

        this._super.apply(this, arguments);
    },

    _onSynologyDownload (ev) {
        ev.stopPropagation();
        ev.preventDefault();
        let path = $(ev.target).data('path');

        this.env.services.rpc({
                model: 'ir.attachment',
                method: 'synology_download',
                kwargs: {
                    path: path,
                },
        }).then( url =>{
            window.location.href = url;
            //window.open(url, '_blank');
        });
    },

    async _onSynologyTree (mode, ev) {
        let path = $(ev.target).data('path');
        if (mode == 'back'){
            let lastIndex=this.res[0].path.lastIndexOf("/");
            path=this.res[0].path.slice(0,lastIndex);
            lastIndex=path.lastIndexOf("/");
            path=path.slice(0,lastIndex);

        }

        if (!path){
            this.res = await this._onSynologyRequest('get_list_share');
            this.res = this.res.data.shares;
            var AttachmentInfo = $(QWeb.render("SynologyTree", {files: this.res, back: false}));
            console.log('res')
            console.log(this.res)
        }
        else{
            this.res = await this._onSynologyRequest('get_file_list', [path]);
            this.res = this.res.data.files;
            var AttachmentInfo = $(QWeb.render("SynologyTree", {files: this.res, back: true}));
            console.log('res')
            console.log(this.res)
        }

        if (this.popup_preview)
            this.popup_preview.close();
        
        this.popup_preview = new Dialog(this, {
            size: 'large',
            dialogClass: 'o_act_window',
            title: _t("Attachments synology picker"),
            $content: AttachmentInfo,
            buttons: [
                {
                    text: _t("Close"), close: true
                }
            ]
        }).open();

        AttachmentInfo.find('.folder').on('click', this._onSynologyTree.bind(this, 'forward'));
        AttachmentInfo.find('.file').on('click', this._onSynologyTree.bind(this, 'forward'));
        AttachmentInfo.find('.oe_button_import_from_synology').on('click', this._onSynologyImport.bind(this));
        AttachmentInfo.find('.oe_button_download_from_synology').on('click', this._onSynologyDownload.bind(this));
        AttachmentInfo.find('.oe_button_back').on('click', this._onSynologyTree.bind(this,'back'));
    },
});

