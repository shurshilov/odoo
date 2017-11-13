/**
*    Copyright 2013 Matthieu Moquet
*    Copyright 2016-2017 LasLabs Inc.
*    License MIT (https://opensource.org/licenses/MIT)
**/

odoo.define('web_widget_darkroom.darkroom_widget', function(require) {
    'use strict';

    var core = require('web.core');
    var session = require('web.session');
    var utils = require('web.utils');

    //var common = require('web.form_common');
    var AbstractField = require('web.AbstractField');
    var base_f = require('web.basic_fields')
    var AbstractWidget = base_f.AbstractFieldBinary
    var imageWidget = base_f.FieldBinaryImage
    //var FieldManagerMixin = require('web.FieldManagerMixin');
    //var mixins = require('web.mixins');
    
    //var _ = require('_');

    var qweb = core.qweb;
    //var form_widget = require('web.form_widgets');
    var form_widget = require('web.FormRenderer');

    // overrie button "save" in modal darkromm for save only coords
    // cropCurrentZone and not real crop for further crop on server side
    var darkroomBut = null;
    form_widget.include({
        _addOnClickAction: function ($el, node) {
            var self = this;
            $el.click(function () {
                //MY CODE
                if(node.attrs.id === "darkroom-save")
                        darkroomBut.darkroom.plugins.crop.cropCurrentZone(true);

                self.trigger_up('button_clicked', {
                    attrs: node.attrs,
                    record: self.state,
                });
            });
        },
    });


/*var ReinitializeWidgetMixin =  {

    start: function() {
        this.initialize_field();
        this._super();
    },
    initialize_field: function() {
        this.on("change:effective_readonly", this, this.reinitialize);
        this.initialize_content();
    },
    reinitialize: function() {
        this.destroy_content();
        this.renderElement();
        this.initialize_content();
    },

    destroy_content: function() {},

    initialize_content: function() {},
};


var ReinitializeFieldMixin =  _.extend({}, ReinitializeWidgetMixin, {
    reinitialize: function() {
        ReinitializeWidgetMixin.reinitialize.call(this);
        if (!this.no_rerender) {
            var res = this.render_value();
            if (this.view && this.view.render_value_defs){
                this.view.render_value_defs.push(res);
            }
        }
    },
});*/

    var FieldDarkroomImage = imageWidget.extend(//ReinitializeFieldMixin,
     {
        className: 'darkroom-widget',
        template: 'FieldDarkroomImage',
        placeholder: "/web/static/src/img/placeholder.png",
        darkroom: null,
        no_rerender: false,

        defaults: {
            // Canvas initialization size
            minWidth: 100,
            minHeight: 100,
            maxWidth: 700,
            maxHeight: 500,
            ratio: null,
            backgroundColor: '#fff',

            // Plugin options
            // shursh mode
            plugins: {
                crop: {
                    minHeight: 150,
                    minWidth: 150,
                    maxHeight: 150,
                    maxWidth: 150,                    
                    ratio: 1
                },
            },
        },

        init: function() {
            this._super.apply(this, arguments);
            this.nodeOptions = _.defaults(this.nodeOptions, this.defaults);
        },

        _init_darkroom: function() {
            if (!this.darkroom) {
                this._init_darkroom_icons();
                this._init_darkroom_ui();
                this._init_darkroom_plugins();
                darkroomBut=this;
            }
        },

        _init_darkroom_icons: function() {
            var element = document.createElement('div');
            element.id = 'darkroom-icons';
            element.style.height = 0;
            element.style.width = 0;
            element.style.position = 'absolute';
            element.style.visibility = 'hidden';
            element.innerHTML = '<!-- inject:svg --><!-- endinject -->';
            this.el.appendChild(element);
        },

        _init_darkroom_plugins: function() {
            require('web_widget_darkroom.darkroom_crop').DarkroomPluginCrop();
            require('web_widget_darkroom.darkroom_history').DarkroomPluginHistory();
            require('web_widget_darkroom.darkroom_rotate').DarkroomPluginRotate();
            require('web_widget_darkroom.darkroom_zoom').DarkroomPluginZoom();
        },

        _init_darkroom_ui: function() {
            // Button object
            function Button(element) {
                this.element = element;
            }

            Button.prototype = {
                addEventListener: function(eventName, listener) {
                    if (this.element.addEventListener) {
                        this.element.addEventListener(eventName, listener);
                    } else if (this.element.attachEvent) {
                        this.element.attachEvent('on' + eventName, listener);
                    }
                },
                removeEventListener: function(eventName, listener) {
                    if (this.element.removeEventListener) {
                        this.element.removeEventListener(eventName, listener);
                    } else if (this.element.detachEvent) {
                        this.element.detachEvent('on' + eventName, listener);
                    }
                },
                active: function(bool) {
                    if (bool) {
                        this.element.classList.add('darkroom-button-active');
                    } else {
                        this.element.classList.remove('darkroom-button-active');
                    }
                },
                hide: function(bool) {
                    if (bool) {
                        this.element.classList.add('hidden');
                    } else {
                        this.element.classList.remove('hidden');
                    }
                },
                disable: function(bool) {
                    this.element.disabled = bool;
                },
            };

            // ButtonGroup object
            function ButtonGroup(element) {
                this.element = element;
            }

            ButtonGroup.prototype = {
                createButton: function(options) {
                    var defaults = {
                        image: 'fa fa-question-circle',
                        type: 'default',
                        group: 'default',
                        hide: false,
                        disabled: false,
                        editOnly: false,
                        addClass: '',
                    };
                    var optionsMerged = Darkroom.Utils.extend(options, defaults);

                    var buttonElement = document.createElement('button');
                    buttonElement.type = 'button';
                    buttonElement.className = 'darkroom-button darkroom-button-' + optionsMerged.type;
                    buttonElement.innerHTML = '<i class="' + optionsMerged.image + ' fa-2x"></i>';
                    if (optionsMerged.editOnly) {
                        buttonElement.classList.add('oe_edit_only');
                    }
                    if (optionsMerged.addClass) {
                        buttonElement.classList.add(optionsMerged.addClass);
                    }
                    this.element.appendChild(buttonElement);

                    var button = new Button(buttonElement);
                    button.hide(optionsMerged.hide);
                    button.disable(optionsMerged.disabled);

                    return button;
                }
            };

            // Toolbar object
            function Toolbar(element) {
                this.element = element;
            }

            Toolbar.prototype = {
                createButtonGroup: function() {
                    var buttonGroupElement = document.createElement('div');
                    buttonGroupElement.className = 'darkroom-button-group';
                    this.element.appendChild(buttonGroupElement);

                    return new ButtonGroup(buttonGroupElement);
                }
            };

            Darkroom.UI = {
                Toolbar: Toolbar,
                ButtonGroup: ButtonGroup,
                Button: Button,
            };
        },

        destroy_content: function() {
            if (this.darkroom && this.darkroom.containerElement) {
                this.darkroom.containerElement.remove();
                this.darkroom = null;
            }
        },

        //set_value: function(value) {
        //    return this._super(value);
        //},

        _render: function () {
            //this.nodeOptions = _.defaults(this.nodeOptions, this.defaults);
            this.destroy_content();
            this._init_darkroom();
            var self = this;
            console.log(this);
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
                        unique: (this.recordData.__last_update || '').replace(/[^0-9]/g, ''),
                    });
                }
            }
            var $img = $('<img>').attr('src', url);
            $img.css({
                width: this.nodeOptions.size ? this.nodeOptions.size[0] : attrs.img_width || attrs.width,
                height: this.nodeOptions.size ? this.nodeOptions.size[1] : attrs.img_height || attrs.height,
            });

                this.$('> img').remove();
                this.$el.prepend($img);
                $img.on('error', function () {
                    self.on_clear();
                    $img.attr('src', self.placeholder);
                    self.do_warn(_t("Image"), _t("Could not display the selected image."));
                });
            //shursh mode
            //this.darkroom = new Darkroom($img.get(0), this.options);
            var opt = _.defaults(this.record.context.options, this.nodeOptions);
            this.darkroom = new Darkroom($img.get(0), opt);
            this.darkroom.widget = this;
            },

        //commit_value: function() {
        //    if (this.darkroom.sourceImage) {
        //        this._set_value(this.darkroom.sourceImage.toDataURL().split(',')[1]);
        //    }
        //},
    });
    console.log("reg11");
    var widgetRegistry = require('web.widget_registry');
    var field_registry = require('web.field_registry');
    var view_registry = require('web.view_registry');

    field_registry.add('darkroom', FieldDarkroomImage);
    //core.form_widget_registry.add("darkroom", FieldDarkroomImage);
    console.log("after reg");

    return {
        //ReinitializeFieldMixin: ReinitializeFieldMixin,
        FieldDarkroomImage: FieldDarkroomImage
    };
});
