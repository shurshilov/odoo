openerp.mail_url = function (ZALUPA_ROBERTA_KUKA) {


    //Change display_attachments URL-only our url, Binary files url in iur server
    ZALUPA_ROBERTA_KUKA.mail.MessageCommon.include({
        
        //changed session.url
        url: function(path, params) {
            params = _.extend(params || {});
            var qs = $.param(params);
            if (qs.length > 0)
                qs = "?" + qs;
            return  path + qs;
        },
        
        //get url for binary files
        get_attachment_url: function (session, message_id, attachment_id) {          
            var model = new ZALUPA_ROBERTA_KUKA.web.Model("ir.attachment");
                return this.url('/mail/download_attachment', {
                    'model': 'mail.message',
                    'id': message_id,
                    'method': 'download_attachment',
                    'attachment_id': attachment_id
                });
        },
               
        display_attachments: function () {
            for (var l in this.attachment_ids) {
                var attach = this.attachment_ids[l];
                if (attach.type == 'url' && !attach.formating) {                                      
                        attach.formating = true;
                    }
                else
                if (!attach.formating) {
                    attach.url = this.get_attachment_url(ZALUPA_ROBERTA_KUKA, this.id, attach.id);
                    attach.name = ZALUPA_ROBERTA_KUKA.mail.ChatterUtils.breakword(attach.name || attach.filename);
                    attach.formating = true;
                }
            }
            this.$(".oe_msg_attachment_list").html( ZALUPA_ROBERTA_KUKA.web.qweb.render('mail.thread.message.attachments', {'widget': this}) );
            console.log("DISPLAY DONE.");
        },
    
    });
  

    ZALUPA_ROBERTA_KUKA.web.form.FieldMany2ManyBinaryMultiFiles.include({
    
        init: function(field_manager, node) {
            this._super(field_manager, node);
            this.fileupload_id2 = _.uniqueId('oe_fileupload_temp');
               console.log(this.fileupload_id);
               console.log(this.fileupload_id2);
            $(window).on(this.fileupload_id2, _.bind(this.on_url_loaded, this));
            
        },
        
        initialize_content: function () {            
            this._super.apply(this);
            var self = this;
           // this.$('span.oe_attach_label.oe_attach_link').on('click', _.bind( this.on_click_label, this));
            this.$('span.oe_attach.oe_attach_link').on('click', _.bind( this.on_click_label, this));
            this.$('span.oe_attach_label.oe_attach_link').on('click', _.bind( this.on_click_label, this));
            this.$('span.oe_e.oe_attach_link').on('click', _.bind( this.on_click_label, this));
            this.$('span.oe_attach_link').on('click', _.bind( this.on_click_label, this));
        //    this.$('input.ui-autocomplete-input.oe_attach').on('change', _.bind( this.on_change_url, this));
        //    this.$('#file_name').on('change', _.bind( this.on_change_filename, this));
        //    this.$('a.oe_right.oe_edit_url.oe_e').on('click', _.bind( this.on_attachment_edit, this));

        },
        
        render_value: function () {
        var self = this;
        this.read_name_values().then(function (ids) {
            var render = $(ZALUPA_ROBERTA_KUKA.web.qweb.render('FieldBinaryFileUploader.files', {'widget': self, 'values': ids}));
            render.on('click', '.oe_delete', _.bind(self.on_file_delete, self));
            render.on('click', '.oe_edit_url', _.bind(self.on_attachment_edit, self));
            self.$('.oe_placeholder_files, .oe_attachments').replaceWith( render );

            //autoclear input field on url loaded 
            var $input_clear = self.$('input.ui-autocomplete-input');
            $input_clear.val('');
            
            // reinit input type file
            var $input = self.$('input.oe_form_binary_file');
            $input.after($input.clone(true)).remove();
            self.$(".oe_fileupload").show();

            });
        },
        
        on_attachment_edit: function (event) {
            var self = this;
            event.stopPropagation();
            var attachment_id=$(event.target).data("id");

            var action = {
                    type: 'ir.actions.act_window',
                    res_model: 'ir.attachment',
                    res_id: attachment_id,
                    view_mode: 'form',
                    view_type: 'form',
                    views: [[false, 'form']],
                    target: 'new',
                    nodestroy: true,
                    flags : {
                    action_buttons : true,
                 //   headless: true,
                    },
                };
                
            function getResults (result) {
                console.log("in action");
                    console.log(result);
            }
            
                self.do_action(action, {
                    'on_close': function(result){ self.ds_attachment = new ZALUPA_ROBERTA_KUKA.web.DataSetSearch(self, 'ir.attachment'); console.log("WORK"); },

                }).done(getResults);               
               
        },
        
        on_click_label: function (event) {
            event.stopPropagation();
            console.log("MY click");
            this.$('input.oe_form_binary_file').click();
        },
  
        on_url_loaded: function (event, result) {
         //   console.log("URL_LOAD");
          //  console.log(result);
          //  console.log(this.model);

            // unblock UI
            if(this.node.attrs.blockui>0) {
                instance.web.unblockUI();
            }
            //ADD some test
            this.data[result.id] = {
                        'id': result.id,
                        'name': result.name,
                        'filename': result.url,
                        'url': result.url
                    };
                
            var values = _.clone(this.get('value'));
            values.push(result.id);
            this.set({'value': values});
            
            this.render_value();
        },
        
        read_name_values : function () {
        var self = this;
        // don't reset know values
        var ids = this.get('value');
        var _value = _.filter(ids, function (id) { return typeof self.data[id] == 'undefined'; } );
        // send request for get_name
        if (_value.length) {
            return this.ds_file.call('read', [_value, ['id', 'name', 'datas_fname','url','type']]).then(function (datas) {
                _.each(datas, function (data) {
                    data.no_unlink = true;
                    if (data.type != 'url')                        
                    data.url = self.session.url('/web/binary/saveas', {model: 'ir.attachment', field: 'datas', filename_field: 'datas_fname', id: data.id});
                    self.data[data.id] = data;
                });
                return ids;
            });
        } else {
            return $.when(ids);
        }
    },

    });


    ZALUPA_ROBERTA_KUKA.mail.ThreadComposeMessage.include({       
  
        start: function () {
            this._super.apply(this, arguments);         
            this.fileupload_id2 = _.uniqueId('oe_fileupload_temp');
            $(window).on(this.fileupload_id2, this.on_url_loaded);
       
        },
        
        // edit the file on the server and reload display         
        on_attachment_edit_url: function (event) {
            var self = this;
            event.stopPropagation();
            var attachment_id=$(event.target).data("id");

            var action = {
                    type: 'ir.actions.act_window',
                    res_model: 'ir.attachment',
                    res_id: attachment_id,
                    view_mode: 'form',
                    view_type: 'form',
                    views: [[false, 'form']],
                    target: 'new',
                    nodestroy: true,
                    flags : {
                    action_buttons : true,
                 //   headless: true,
                    },
                };
                
            function getResults (result) {
                console.log("in action");
                    console.log(result);
            }
            
                self.do_action(action, {
                    'on_close': function(result){ self.ds_attachment = new ZALUPA_ROBERTA_KUKA.web.DataSetSearch(self, 'ir.attachment'); self.display_attachments(); console.log("WORK"); },

                }).done(getResults);
                
                
                self.display_attachments();
        },
        
        bind_events: function () {            
            this._super.apply(this);
            var self = this;
            // Click button or icon or label --> click file_input
            this.$('span.oe_attach_label.oe_attach_link').on('click', _.bind( this.on_click_label, this));
            this.$('span.oe_e.oe_attach_link').on('click', _.bind( this.on_click_label, this));
            this.$('span.oe_attach_link').on('click', _.bind( this.on_click_label, this));
 
            // event: EDIT child attachments off the oe_msg_attachment_list box
            this.$(".oe_msg_attachment_list").on('click', '.oe_edit_url', this.on_attachment_edit_url);

        },
        
        on_click_label: function (event) {
            //console.log("MY click mail.js");
            this.$('input.oe_form_binary_file').click();
        },
        
        on_change_url: function (event) {
            //console.log("MY change mail.js");
           // this.$('input.ui-autocomplete-input.oe_attach').val(this.$('input.ui-autocomplete-input').val());

        },       
        
        on_url_loaded: function (event, result) {

            this.attachment_ids.push({
                    'id': 0,
                    'name': result.name,
                    'filename': "link",
                    'url': result.url,
                    'upload': true
                });
            
            //console.log(result);
            if (result.error || !result.id ) {
                this.do_warn( ZALUPA_ROBERTA_KUKA.web.qweb.render('mail.error_upload'), result.error);
                this.attachment_ids = _.filter(this.attachment_ids, function (val) { return !val.upload; });
            } else {
                for (var i in this.attachment_ids) {
                    if (this.attachment_ids[i].name == result.name && this.attachment_ids[i].upload) {
                        this.attachment_ids[i]={
                            'id': result.id,
                            'name': result.name,
                            'filename': false,
                            'url': result.url,
                            'is_url': true,
                            'type': result.type,
                        };
                    }
                }
            }            
            
            this.display_attachments();
            
            //autoclear input field on url loaded 
            var $input = this.$('input.ui-autocomplete-input');
            $input.val('');
            
            this.$(".oe_attachment_file").show();
            //console.log("URL LOAD IN MAIL DONE");
        },
        
        // ADD autoclear input field on file loaded      
        on_attachment_loaded: function (event, result) {
            this._super(event, result);
            var $input = this.$('input.ui-autocomplete-input');
            $input.val('');       
        },
        
    });

};


