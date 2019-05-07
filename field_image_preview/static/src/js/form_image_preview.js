
odoo.define('field_image_preview.image_widget_extend', function (require) {
"use strict";

    var core = require('web.core');
    var base_f = require('web.basic_fields')
    //var imageWidget = core.form_widget_registry.get('image');
	var imageWidget = base_f.FieldBinaryImage
    var session = require('web.session');
    var utils = require('web.utils');
    var qweb = core.qweb;
    // check bug 17.01.18
    var field_utils = require('web.field_utils');
    var DocumentViewer = require('mail.DocumentViewer');

imageWidget.include({

    _render: function () {
                var self = this;
        var url = this.placeholder;
        if (this.value) {
            if (!utils.is_bin_size(this.value)) {
                // Use magic-word technique for detecting image type
                url = 'data:image/' + (this.file_type_magic_word[this.value[0]] || 'png') + ';base64,' + this.value;
            } else {
                url = session.url('/web/image', {
                    model: this.model,
                    id: JSON.stringify(this.res_id),
                    field: this.nodeOptions.preview_image || this.name,
                    // unique forces a reload of the image when the record has been updated
                    unique: field_utils.format.datetime(this.recordData.__last_update).replace(/[^0-9]/g, ''),
                });
            }
        }
        var $img = $(qweb.render("FieldBinaryImage-img", {widget: this, url: url}));
        // override css size attributes (could have been defined in css files)
        // if specified on the widget
        var width = this.nodeOptions.size ? this.nodeOptions.size[0] : this.attrs.width;
        var height = this.nodeOptions.size ? this.nodeOptions.size[1] : this.attrs.height;
        if (width) {
            $img.attr('width', width);
            $img.css('max-width', width + 'px');
        }
        if (height) {
            $img.attr('height', height);
            $img.css('max-height', height + 'px');
        }
        this.$('> img').remove();
        this.$el.prepend($img);
        $img.on('error', function () {
            self._clearFile();
            $img.attr('src', self.placeholder);
            self.do_warn(_t("Image"), _t("Could not display the selected image."));
        });

        //Odoo save 3 variant of image, just image is original also have medium and small
        var imgSrc = this.placeholder;
        if (this.value) {
            if (!utils.is_bin_size(this.value)) {
                // Use magic-word technique for detecting image type
                imgSrc = 'data:image/' + (this.file_type_magic_word[this.value[0]] || 'png') + ';base64,' + this.value;
            } else {
                imgSrc = session.url('/web/image', {
                    model: this.model,
                    id: JSON.stringify(this.res_id),
                    field: "image" || this.nodeOptions.preview_image || this.name,
                    // unique forces a reload of the image when the record has been updated
                    unique: field_utils.format.datetime(this.recordData.__last_update).replace(/[^0-9]/g, ''),
                });
            }
        }
        //Click code, open in new popup in ORIGINAL size, minimum size popup 500x500 in css
        $($img).click(function(e) {

/*        var activeAttachmentID = $(e.currentTarget).data('id');
        var attachments = this.get('attachment_ids');
        if (activeAttachmentID) {
            var attachmentViewer = new DocumentViewer(this, attachments, activeAttachmentID);
            attachmentViewer.appendTo($('body'));
        }*/



            var a = $('#outer').find('img')[0]
            if (a) a.remove();
            $('#outer').prepend('<img id="inner" src="'+imgSrc+'" />');
            //change css of parent because class oe_avatar 90x90 size maximum
            $('#outer').find('img').parent().css=({
            	width:'100%',
            	height:'100%',            
        	});         
            $('#outer').fadeIn('slow');
    
            $('#outer').click(function(e)
            {
            	self.$('#inner').remove();
                $(this).fadeOut();

            });

           $(document).mouseup(function (e){ // action click on web-document
          	  self.$('#inner').remove();
              var div = $("#outer"); // ID-element
              if (!div.is(e.target) // if click NO our elementе
              && div.has(e.target).length === 0) { // and NO our children elemets
              div.hide();

             }
           });
        });
    },
});
});

