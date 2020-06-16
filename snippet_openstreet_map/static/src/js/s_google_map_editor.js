odoo.define('snippet_openstreet_map.s_google_map_editor', function (require) {
    'use strict';

    var ajax = require('web.ajax');
    var Dialog = require("web_editor.widget").Dialog;
    var core = require('web.core');
    var s_options = require('web_editor.snippets.options');
    var googleScriptLoaded = require("snippet_openstreet_map.s_google_map_frontend").googleScriptLoaded;

    var _t = core._t;

    ajax.loadXML('/snippet_openstreet_map/static/src/xml/s_google_map_modal.xml', core.qweb);

    s_options.registry.map = s_options.Class.extend({
/*        start: function () {
            this.$filterValueOpts = this.$el.find('[data-map_zoom]');
            console.log("EDITOR");
            console.log(this.$filterValueOpts);

            return this._super.apply(this, arguments);
        },*/

        default_location: "(55.75, 37.62)",

        map: function (previewMode, value, $li) {
            var self = this;

            this.dialog = new Dialog(this, {
                size: "medium",
                title: _t("Customize your map"),
                buttons: [
                    {text: _t("Save"), classes: "btn-primary", close: true, click: function () {
                        if (!this.$("#center-map").val()) {
                            this.$("#center-map").val(self.default_location);
                        }
                        self.$target.attr({
                            "data-map-gps": this.$("#center-map").val(),
                            "data-pin-style": this.$("#pin_style").val(),
                            "data-markers": this.$("#markers").val(),
                            "data-map-zoom": this.$("#zoom").val(),
                        });
                        //self.$target.data("snippet-view").redraw();
                    }},
                    {text: _t("Cancel"), close: true}
                ],
                $content: $(core.qweb.render("snippet_openstreet_map.s_google_map_modal"))
            });

            this.dialog.opened().then((function () {
                this.$("#center-map").val(self.$target.attr('data-map-gps'));
                this.$("#pin_style").val(self.$target.attr('data-pin-style'));
                this.$("#markers").val(self.$target.attr('data-markers'));
                this.$("#zoom").val(self.$target.attr('data-map-zoom'));
            }).bind(this.dialog));

            self.dialog.open();
        },

        map_type: function (previewMode, value, $li) {
            this.$target.attr('data-map-type', value);
            this.$target.attr('data-map-color', "");
            //this.$target.data('snippet-view').redraw();
        },

        map_color: function (previewMode, value, $li) {
            this.$target.attr('data-map-color', value);
            //this.$target.data('snippet-view').redraw();
        },

        map_zoom: function (previewMode, value, $li) {
            this.$target.attr('data-map-zoom', value);
            //this.$target.data('snippet-view').redraw();
        },

        map_gps: function (previewMode, value, $li) {
            this.$target.attr('data-map-gps', value);
            //this.$target.data('snippet-view').redraw();
        },

        _setActive: function () {
            this.$el.find('[data-map_type]')
                .removeClass('active')
                .filter('[data-map_type="'+this.$target.attr('data-map-type')+'"]')
                .addClass('active');
            this.$el.find('[data-map_color]')
                .removeClass('active')
                .filter('[data-map_color="'+this.$target.attr('data-map-color')+'"]')
                .addClass('active');
            this.$el.find('[data-map_zoom]')
                .removeClass('active')
                .filter('[data-map_zoom="'+this.$target.attr('data-map-zoom')+'"]')
                .addClass('active');
            this.$el.find('[data-map_gps]')
                .removeClass('active')
                .filter('[data-map_gps="'+this.$target.attr('data-map-gps')+'"]')
                .addClass('active');
        },

        onBuilt: function () {
            this._super.apply(this, arguments);
            this.map('click', null, null);
        },
    });
});
