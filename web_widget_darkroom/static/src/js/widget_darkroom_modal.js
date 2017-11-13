/**
*    Copyright 2017 LasLabs Inc.
*    License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
**/

odoo.define('web_widget_darkroom.darkroom_modal_button', function(require) {
    'use strict';

    var core = require('web.core');
    var base_f = require('web.basic_fields')
    var imageWidget = base_f.FieldBinaryImage
    var rpc = require('web.rpc');
    //var DataModel = require('web.DataModel');

    imageWidget.include({
        // Used in template to prevent Darkroom buttons from being added to
        // forms for new records, which are not supported
        darkroom_supported: function() {
            if (this.field_manager.dataset.index === null) {
                return false;
            }
            return true;
        },

        on_file_uploaded_and_valid: function(size, name, content_type, file_base64) {
            this._super();
            //shursh mode current image in context to modal 
            //and update coords and give options to Darkroom widget
            if ('plugins' in this.nodeOptions)
            {
                var imageWidget = this;
                var activeModel = imageWidget.record.model;
                var activeRecordId = imageWidget.record.data.id;
                var activeField = imageWidget.attrs.name;
                var coordsField = imageWidget.nodeOptions.plugins.crop.coords;
 /*               console.log(activeModel);
                console.log(activeRecordId);
                console.log(activeField);
                console.log(coordsField);*/
                //on close modal or click "save burron" update image and coords field by js query AJAX
                var updateImage = function() {
                    rpc.query({
                            model: activeModel,
                            method: 'read',
                            args: [[activeRecordId], [activeField,coordsField]],
                    })
                    .then(function(result){
                                console.log(imageWidget);
                                console.log("1111");
                                imageWidget._setValue(result[0][imageWidget.attrs.name]);
                                if (coordsField){
                                    //var field = imageWidget.record.fields[coordsField];
                                    var field = imageWidget.fields[coordsField];
                                    imageWidget.record.data[coordsField] =result[0][coordsField];
                                    imageWidget.recordData[coordsField] =result[0][coordsField];
                                    //field.value=result[0][coordsField];
                                    console.log(field);
                                    console.log("2223");
                                    //console.log(field.__defineSetter__);
                                }
                    });
                };

                var openModal = function() {
                    var context = {
                        active_model: activeModel,
                        active_record_id: activeRecordId,
                        active_field: activeField,
                        //give current image and options from Image widget to Darkroom widget by ctx
                        current_image: file_base64,
                        options: imageWidget.nodeOptions,
                    };
                    var modalAction = {
                        type: 'ir.actions.act_window',
                        res_model: 'darkroom.modal',
                        name: 'Darkroom',
                        views: [[false, 'form']],
                        target: 'new',
                        context: context,
                    };
                    var options = {on_close: updateImage};
                    imageWidget.do_action(modalAction, options);
                };
                openModal();
            }
    },
    });
});
