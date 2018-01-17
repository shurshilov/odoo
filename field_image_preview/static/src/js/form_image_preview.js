
odoo.define('field_image_preview.image_widget_extend', function (require) {
"use strict";

    var core = require('web.core');
    var base_f = require('web.basic_fields')
    //var imageWidget = core.form_widget_registry.get('image');
	var imageWidget = base_f.FieldBinaryImage
    var session = require('web.session');
    var utils = require('web.utils');
    var QWeb = core.qweb;
    // check bug 17.01.18
    var field_utils = require('web.field_utils');

imageWidget.include({

    _render: function () {
        var self = this;
        var attrs = this.attrs;
        var url = this.placeholder;
        if (this.value) {
            if (!utils.is_bin_size(this.value)) {
                url = 'data:image/png;base64,' + this.value;
            } else {
                url = session.url('/web/image', {
                    model: this.model,
                    id: JSON.stringify(this.res_id),
                    field: this.nodeOptions.preview_image || this.name,
                    // unique forces a reload of the image when the record has been updated
                    //unique: (this.recordData.__last_update || '').replace(/[^0-9]/g, ''),
			// check bug 17.01.18
	              unique: field_utils.format.datetime(this.recordData.__last_update).replace(/[^0-9]/g, ''),
                });
            }
        }
        var $img = $('<img>').attr('src', url);
        $img.css({
            width: this.nodeOptions.size ? this.nodeOptions.size[0] : attrs.img_width || attrs.width,
            height: this.nodeOptions.size ? this.nodeOptions.size[1] : attrs.img_height || attrs.height,
        });

        //Odoo save 3 variant of image, just image is original also have medium and small
        var imgSrc = this.placeholder;
        if (this.value) {
            if (!utils.is_bin_size(this.value)) {
                imgSrc = 'data:image/png;base64,' + this.value;
            } else {
                var field = this.nodeOptions.preview_image || this.name;
                if (field == "image_medium" ||
                field == "image_small")                
                field = "image";
            	console.log(field);
            	console.log(imgSrc);


                imgSrc = session.url('/web/image', {
                    model: this.model,
                    id: JSON.stringify(this.res_id),
                    field: field,
                    // unique forces a reload of the image when the record has been updated
                   // unique: (this.recordData.__last_update || '').replace(/[^0-9]/g, ''),
		   // check bug 17.01.18
	              unique: field_utils.format.datetime(this.recordData.__last_update).replace(/[^0-9]/g, ''),
                });
                console.log(imgSrc);
            }
        }
        
        //Click code, open in new popup in ORIGINAL size, minimum size popup 500x500 in css
        $($img).click(function(e) {
/*           if(self.view.get("actual_mode") == "view") {
                var $button = $(".oe_form_button_edit");
                $button.openerpBounce();
                e.stopPropagation();
            }
*/
            // set attr SRC image, in our hidden div
            //console.log("bla 2");
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
            
            
        //!!!!!!!!!!!
        //this.$('#outer').remove();
        this.$('> img').remove();
       // this.$('#inner').remove();
        this.$el.prepend($img);
        $img.on('error', function () {
            self.on_clear();
            $img.attr('src', self.placeholder);
            self.do_warn(_t("Image"), _t("Could not display the selected image."));
        });
    },


});

});
