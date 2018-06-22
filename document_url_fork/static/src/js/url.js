odoo.define('document_url_fork.document_url_fork', function (require) {
"use strict";

    var core = require('web.core');
    var _t = core._t;
    var QWeb = core.qweb;
    var Sidebar = require('web.Sidebar');
    var ActionManager = require('web.ActionManager');

    Sidebar.include({
        _redraw: function() {
            var self = this;
            this._super.apply(this, arguments);
            self.$el.find('.o_sidebar_add_attachment').after(QWeb.render('AddUrlDocumentItem', {widget: self}))
            self.$el.find('.oe_sidebar_add_url').on('click', function (e) {
                self.on_url_doc();
            });
        },
        on_url_doc: function() {
            var self = this;

            var activeModel = self.env.model;
            var activeRecordId = self.getParent().renderer.state.data.id;

            var openModal = function() {
                    var context = {
                        active_model: activeModel,
                        active_record_id: activeRecordId,
                        //active_field: activeField,
                    };
                    var modalAction = {
                        type: 'ir.actions.act_window',
                        res_model: 'ir.attachment.add_url',
                        name: 'ADD URL',
                        views: [[false, 'form']],
                        target: 'new',
                        context: context,
                    };
                    self.do_action(modalAction);
                };
                openModal();
        },
    });

    ActionManager.include({
        ir_actions_act_close_wizard_and_reload_view: function (action, options) {
            if (!this.dialog) {
                options.on_close();
            }
            this.dialog_stop();
            this.inner_widget.active_view.controller.reload()
            return $.when();
        },
    });

});
