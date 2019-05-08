
odoo.define('field_image_preview.image_widget_extend', function (require) {
"use strict";

    var base_f = require('web.basic_fields')
	var imageWidget = base_f.FieldBinaryImage
    var DocumentViewer = require('mail.DocumentViewer');

imageWidget.include({

    _render: function () {
        this._super.apply(this, arguments);
        var self = this;
        this.$("img").click(function(e) {
            // console.log(self);
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
    },
});
});

