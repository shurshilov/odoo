/**
*    Copyright 2017 LasLabs Inc.
*    Copyright 2017-2018 Artem Shurshilov
*    License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
**/

odoo.define('web_widget_darkroom.darkroom_modal_button', function(require) {
    'use strict';

    var core = require('web.core');
    var DataModel = require('web.DataModel');
    var QWeb = core.qweb;
    var $ = require('$');
    var _t = core._t;

    core.form_widget_registry.get('image').include({
        // Used in template to prevent Darkroom buttons from being added to
        // forms for new records, which are not supported
        darkroom_supported: function() {
            if (this.field_manager.dataset.index === null) {
                return false;
            }
            return true;
        },

        initialize_content: function() {
            var self= this;
            //classic code
            this.$('input.o_form_input_file').change(this.on_file_change);
            this.$('button.oe_form_binary_file_save').click(this.on_save_as);
            this.$('.oe_form_binary_file_clear').click(this.on_clear);
            //override 4 button
            this.$('.oe_form_binary_file_upload').click(function() {
                self.$('input.o_form_input_file').click();
            });
            this.$('.oe_form_binary_file_edit').click(function() {
                self.openModal(null, {'click':'crop'});
            });
            this.$('.oe_form_binary_file_eye').click(function() {
                self.openModal(null, {'click':'zoom'});
            });
            this.$('.oe_form_binary_file_back').click(function() {
                self.back();
            });
            //***from ir_attachment_url
            this.url_clicked = false;
            this.is_url = false;
            this.imgSrc = false;
            this.$('.oe_link_address_button').click(function() {
                self.on_link_address();
            });
        },

        // On close modal or click "save burron" update image by read js rpc
        updateImage: function() {
            var self = this;
            var ctx = self.getContext();
            var ActiveModel = new DataModel(ctx.active_model);
            //set origin image
            if (ctx.active_field === 'image_medium')
                ctx.active_field = 'image';
            ActiveModel.query([ctx.active_field]).
                filter([['id', '=', ctx.active_record_id]]).
                all().
                then(function(result) {
                    self.set_value(result[0][ctx.active_field]);
                });
        },

        openModal: function(file_base64, clickDefault) {
            var self = this;
            var context = self.getContext();
            if (file_base64)
                //give current image and options from Image widget to Darkroom widget by context
                context.current_image = file_base64
            else
                //context for python function _default_image, open original image, not medium or small
                context.size_image = 'image';
            if (clickDefault)
                context.click = clickDefault.click;
            //console.log("openModal");
            //console.log(context);
            var modalAction = {
                type: 'ir.actions.act_window',
                res_model: 'darkroom.modal',
                name: 'Darkroom',
                views: [[false, 'form']],
                target: 'new',
                context: context,
            };
            var updateImage =  function() {
                self.updateImage();
            };
            var options = {on_close: updateImage};
            self.do_action(modalAction, options);
        },

        getContext: function() {
            var self = this;
            var activeModel = self.field_manager.dataset._model.name;
            var activeRecordId = self.field_manager.datarecord.id;
            var activeField = self.node.attrs.name;
            return {
                active_model: activeModel,
                active_record_id: activeRecordId,
                active_field: activeField,
                options: self.options,
            };
        },
        on_file_uploaded_and_valid: function(size, name, content_type, file_base64) {
            var self = this;
            this.internal_set_value(file_base64);
            this.binary_value = true;
            this.render_value();
            this.set_filename(name);

            //shursh mode current image in context to modal 
            //and give options to Darkroom widget
            self.openModal(file_base64, {'click':'crop'});
        },
        render_value: function() {
            var self = this;
            if (this.url_clicked) {
                this.$el.children("img[name='image_medium']").remove();
                this.$el.children(".input_url").remove();
                this.$el.prepend($(QWeb.render("AttachmentURL", {widget: this})));
                this.$input = this.$(".input_url input");
            } else {
                this.$el.children(".input_url").remove();
                this._super();
                //***from web_widget_image_download
                var $widget = this.$el.find('.oe_form_binary_file_download');
                var image = this.$el.find('img[name="' + this.name + '"]');
                if (image.attr('src')){
                    this.imgSrc = image.attr('src');
                    this.imgSrc = this.imgSrc.replace('image_medium','image').toString();
                    //original size href with target=_blank
                    $widget.attr('href', this.imgSrc);
                    $widget.attr('download', 'image.png');
                    this.$el.find('.oe_form_binary_file_expand').attr('href', this.imgSrc);
                }
                //***from field_image_preview
                $(image).click(function(e) {
                    if(self.view.get("actual_mode") == "view") {
                        var $button = $(".oe_form_button_edit");
                        $button.openerpBounce();
                        e.stopPropagation();
                    }
                    // set attr SRC image, in our hidden div
                    $('#inner').attr({src: self.imgSrc});
                    $('#outer').fadeIn('slow');
                    $('#outer').click(function(e)
                    {
                        $(this).fadeOut();
                    });
                    $(document).mouseup(function (e){ // action click on web-document
                        var div = $("#outer"); // ID-element
                        if (!div.is(e.target) // if click NO our elementе
                           && div.has(e.target).length === 0) { // and NO our children elemets
                                div.hide(); 
                        }
                    });
                    
                });
                //this.$el.find('#outer').remove();
            }

            
        },
        //***from ir_attachment_url
        store_dom_url_value: function () {
            if (this.$input && this.$input.val()) {
                if (this.is_url_valid()) {
                    this.set_value(this.$input.val());
                } else {
                    this.do_warn(_t('Warning'), _t('URL is invalid.'));
                }
            }
        },
        back: function() {
            this.is_url = false;
            this.url_clicked = false;
            this.set_filename(this.imgSrc);
            this.render_value();           
        },
        on_link_address: function() {
            this.is_url = true;
            if (!this.url_clicked) {
                this.url_clicked = true;
                this.render_value();
            } else if (this.url_clicked) {
                this.url_clicked = false;
                this.render_value();
            }
           
        },
        commit_value: function () {
            if (this.is_url) {
                this.store_dom_url_value();
                this.is_url = false;
            }
            return this._super();
        },
        is_url_valid: function() {
            if (this.$input.is('input')) {
                var u = new RegExp("^(http[s]?:\\/\\/(www\\.)?|ftp:\\/\\/(www\\.)?|www\\.){1}([0-9A-Za-z-\\.@:%_~#=]+)+((\\.[a-zA-Z]{2,3})+)(/(.)*)?(\\?(.)*)?");
                return u.test(this.$input.val());
            }
            return true;
        },

    });
});
