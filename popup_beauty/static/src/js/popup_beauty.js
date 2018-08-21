odoo.define('popup_beauty', function (require) {
"use strict";

    var core = require('web.core');
    var Widget = require('web.Widget');
    var ControlPanelMixin = require('web.ControlPanelMixin');
    var data = require('web.data');
    var qweb = core.qweb;

    var BeautyPopup = Widget.extend(ControlPanelMixin, {
        events: { 
                'click button.btn': 'close',                
                },

        init: function(parent, action, options) {
            this._super.apply(this, arguments);
            this.action = action;
            this.action_manager = parent;
        },

/*      // TODO load parent view. Now append parent innerHTML:)
        willStart: function () {
            var self = this;
            var view_id = this.action && this.action.search_view_id && this.action.search_view_id[0];
            var def = this
                .loadViews('delivery_dpd_express_beta_list',  new data.CompoundContext(this.action.context || {}), [[view_id, 'search']])
                .then(function (result) {
                    self.fields_view = result.search;
                });
            return $.when(this._super(), def);
        },*/

        start: function(){
            this.$el.append(qweb.render('BeautyPopup', {
                body: this.action.context.body,
                button: this.action.context.button,
                type: this.action.context.type,
            }));
            //TODO fix. need load view or other tric
            this.$el.append(this.getParent().$el[0].innerHTML);
            this.close_link = this.getParent().$el[0].baseURI;
        },

        close: function(){
            document.location.href=this.close_link;
        },
    });

    core.action_registry.add('popup_beauty.new', BeautyPopup);
});