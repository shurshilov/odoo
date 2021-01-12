/**
*    Copyright 2017 LasLabs Inc.
*    Copyright 2017-2018 Shurshilov Artem
*    License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
**/

odoo.define('web_widget_darkroom.darkroom_modal_button', function(require) {
    'use strict';

    var core = require('web.core');
    var rpc = require('web.rpc');
    var qweb = core.qweb;
    var QWeb = require('web.QWeb');
    var _t = core._t;
    var base_f = require('web.basic_fields');
    var imageWidget = base_f.FieldBinaryImage;
    var AbstractFieldBinary = base_f.AbstractFieldBinary;
    var session = require('web.session');
    var utils = require('web.utils');
    var field_utils = require('web.field_utils');
    var rpc = require('web.rpc');
    var Context = require('web.Context');
    var DocumentViewer = require('mail.DocumentViewer');

/*	AbstractFieldBinary.include({

	});*/
    imageWidget.include({
        events: _.extend({}, imageWidget.prototype.events, {
            //add 4 new button, override 1 button
            'click .oe_form_binary_file_upload': function () {
                this.$('.o_input_file').click();
            },
            'click .oe_form_binary_file_edit': function () {
                this.openModal(null, {'click':'crop'});
            },
            'click .oe_form_binary_file_eye': function () {
                this.openModal(null, {'click':'zoom'});
            },
            'click .oe_form_binary_file_back': function () {
                this.back();
            },
            'click .oe_form_binary_file_clear': 'on_clear',
            //***from ir_attachment_url
            'click .oe_link_address_button': function () {
                this.on_link_address();
            },
        }),
        // Used in template to prevent Darkroom buttons from being added to
        // forms for new records, which are not supported
        darkroom_supported: function() {
            //console.log(this);
/*            if (this.field_manager.dataset.index === null) {
                return false;
            }*/
            return true;
        },

        // On close modal or click "save button" update image by read js rpc
        updateImage: function(result) {
            console.log("update");
            console.log(this);
            console.log(result);
            var self = this;
            var ctx = self.getContext();
            console.log(ctx);
            if (ctx.active_field === 'image_medium')
                ctx.active_field = 'image';

            return rpc.query({
                        model: ctx.active_model,
                        method: 'search_read',
                        args: [
                        	[['id', '=', ctx.active_record_id]], 
                        	[ctx.active_field]
                        ],
                        context: new Context(),
                    })
            .then(function(result){
            	console.log(result);
                    result.forEach(function(result){
                        self._setValue(result[ctx.active_field]);
                        //self._render();
                    });
                });
        },

        openModal: function(file_base64, clickDefault) {
            var self = this;
            var context = self.getContext();
            if (file_base64)
                //give current image and options from Image widget to Darkroom widget by context
                context.current_image = file_base64;
            else
                //context for python function _default_image, open original image, not medium or small
                context.size_image = 'image';
            if (clickDefault)
                context.click = clickDefault.click;
            //context.widget_image = "23423";

            var modalAction = {
                type: 'ir.actions.act_window',
                res_model: 'darkroom.modal',
                name: 'Widget image editor',
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
            return {
                active_model: this.model,
                active_record_id: this.res_id,
                active_field: this.attrs.name,
                options: this.nodeOptions,
            };
        },
        on_file_change: function (e) {
	        var self = this;
	        var file_node = e.target;
	        if ((this.useFileAPI && file_node.files.length) || (!this.useFileAPI && $(file_node).val() !== '')) {
	            if (this.useFileAPI) {
	                console.log(file_node);
	                var file = file_node.files[0];
	                if (file.size > this.max_upload_size) {
	                    var msg = _t("The selected file exceed the maximum file size of %s.");
	                    this.do_warn(_t("File upload"), _.str.sprintf(msg, utils.human_size(this.max_upload_size)));
	                    return false;
	                }
	                var filereader = new FileReader();
	                filereader.readAsDataURL(file);
	                filereader.onloadend = function (upload) {
	                    var data = upload.target.result;
	                    data = data.split(',')[1];
	                    self.on_file_uploaded(file.size, file.name, file.type, data);
	                };
	            } else {
	                this.$('form.o_form_binary_form input[name=session_id]').val(this.getSession().session_id);
	                this.$('form.o_form_binary_form').submit();
	            }
	            this.$('.o_form_binary_progress').show();
	            this.$('button').hide();
	        }
	    },
        on_file_uploaded_and_valid: function(size, name, content_type, file_base64) {
        	this._super.apply(this, arguments);
            //shursh mode current image in context to modal 
            //and give options to Darkroom widget
            this.openModal(file_base64, {'click':'crop'});
        },
        _render: function() {
            //console.log("213");
            var self = this;
            if (this.is_url_valid(this.value)) {
                    console.log("найден URL");
                    var attrs = this.attrs;
                    var url = this.placeholder;
                    if (this.value) {
                        url = this.value;
                    }
                    var $img = $('<img>').attr('src', url);
                    $img.css({
                        width: this.nodeOptions.size
                        ? this.nodeOptions.size[0]
                        : attrs.img_width || attrs.width,
                        height: this.nodeOptions.size
                        ? this.nodeOptions.size[1]
                        : attrs.img_height || attrs.height,
                    });
                    this.$('> img').remove();
                    this.$el.prepend($img);
                    $img.on('error', function () {
                        self.on_clear();
                        $img.attr('src', self.placeholder);
                        self.do_warn(_t("Image"), _t("Could not display the selected image."));
                    }); 
            }
            else {
                this.$el.children(".input_url").remove();
                this._super.apply(this, arguments);
                if (!this.imgSrc)    {    
                this.imgSrc = this.placeholder;
                this.value_old = this.value;}
                if (this.value) {
                    if (!utils.is_bin_size(this.value)) {
                        this.imgSrc = 'data:image/png;base64,' + this.value;
                    } else {
                        var field = this.nodeOptions.preview_image || this.name;
                        if (field == "image_medium" ||
                        field == "image_small")                
                        field = "image";
                        this.imgSrc = session.url('/web/image', {
                            model: this.model,
                            id: JSON.stringify(this.res_id),
                            field: field,
                            // unique forces a reload of the image when the record has been updated
                            // unique: (this.recordData.__last_update || '').replace(/[^0-9]/g, ''),
                            // check bug 17.01.18
                          unique: field_utils.format.datetime(this.recordData.__last_update).replace(/[^0-9]/g, ''),
                        });
                    }
                }
                //***from web_widget_image_download
                var $widget = this.$el.find('.oe_form_binary_file_download');
                $widget.attr('href', this.imgSrc);
                $widget.attr('download', 'image.png');

                //original size href with target=_blank
                this.$el.find('.oe_form_binary_file_expand').attr('href', this.imgSrc);
            
                //***from field_image_preview
                var image = this.$el.find('img[name="' + this.name + '"]');
                $(image).click(function(e) {
                    var source_id = self.model + "/" + JSON.stringify(self.res_id) +"/image";
                    var attachments = [{
                        "filename": self.recordData.display_name ,
                        "id": source_id,
                        "is_main": true,
                        "mimetype": "image/jpeg",
                        "name": self.recordData.display_name + " " + self.value,
                        "type": "image",
                    }]
                    var attachmentViewer = new DocumentViewer(self, attachments, source_id);
                    attachmentViewer.appendTo($('body'));
                        
                });
            }
            
        },
        back: function() {
            //this.set_filename(this.imgSrc);
            this._setValue(this.value_old);
            this._render();           
        },
        //***from ir_attachment_url
        on_link_address: function() {
            var self = this;
            this.$el.children(".img-responsive").remove();
            this.$el.children(".input_url").remove();
            this.$el.children(".o_form_image_controls").addClass("media_url_controls");
            this.$el.prepend($(qweb.render("AttachmentURL", {widget: this})));
            this.$('.input_url input').on('change', function() {
                var input_val = $(this).val();
                self._setValue(input_val);
            });
        },
        is_url_valid: function(value) {
            if (value || (this.$input && this.$input.is('input'))) {
                var u = new RegExp("^(http[s]?:\\/\\/(www\\.)?|ftp:\\/\\/(www\\.)?|www\\.){1}([0-9A-Za-z-\\.@:%_~#=]+)+((\\.[a-zA-Z]{2,3})+)(/(.)*)?(\\?(.)*)?");
                return u.test(value || this.$input.val());
            }
            return false;
        },

    });
});
