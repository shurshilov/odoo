openerp.document_url = function (ZALUPA_ROBERTA_KUKA) {
    
    
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
        //    this.$('.span.oe_attach_label.oe_attach_link').on('click', self.on_attachment_loaded);
            this.$('span.oe_attach_label.oe_attach_link').on('click', _.bind( this.on_click_label, this));
            this.$('span.oe_e.oe_attach_link').on('click', _.bind( this.on_click_label, this));
            this.$('input.ui-autocomplete-input.oe_attach').on('change', _.bind( this.on_change_url, this));

        },
        
        on_click_label: function (event) {
            console.log("MY click");
            this.$('input.oe_form_binary_file').click();
        },
        
        on_change_url: function (event) {
            console.log("MY change");
            this.$('input.ui-autocomplete-input').val("http://"+this.$('input.ui-autocomplete-input').val());

        },
        
        on_url_loaded: function (event, result) {
            console.log("URL_LOAD");
            console.log(result);
            console.log(this.model);

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

    });
    
    var mail = ZALUPA_ROBERTA_KUKA.mail;
    mail.ThreadComposeMessage = mail.ThreadComposeMessage.extend({   
    
  
        start: function () {
            this._super.apply(this, arguments);         
            this.fileupload_id2 = _.uniqueId('oe_fileupload_temp');
                console.log("ON COMPOSE");
               console.log(this.fileupload_id);
               console.log(this.fileupload_id2);
            $(window).on(this.fileupload_id2, this.on_url_loaded);
       
        },
        
        bind_events: function () {            
            this._super.apply(this);
            var self = this;
        //    this.$('.span.oe_attach_label.oe_attach_link').on('click', self.on_attachment_loaded);
            this.$('span.oe_attach_label.oe_attach_link').on('click', _.bind( this.on_click_label, this));
            this.$('span.oe_e.oe_attach_link').on('click', _.bind( this.on_click_label, this));
            this.$('input.ui-autocomplete-input.oe_attach').on('change', _.bind( this.on_change_url, this));

        },
        
        on_click_label: function (event) {
            console.log("MY click");
            this.$('input.oe_form_binary_file').click();
        },
        
        on_change_url: function (event) {
            console.log("MY change");
            this.$('input.ui-autocomplete-input').val("http://"+this.$('input.ui-autocomplete-input').val());

        },
        
        
        
        on_url_loaded: function (event, result) {

             this.attachment_ids.push({
                    'id': 0,
                    'name': result.name,
                    'filename': "link",
                    'url': result.url,
                    'upload': true
                });
            console.log("URL LOAD IN COMPOSE");
             console.log(result);
            if (result.error || !result.id ) {
                this.do_warn( ZALUPA_ROBERTA_KUKA.web.qweb.render('mail.error_upload'), result.error);
                this.attachment_ids = _.filter(this.attachment_ids, function (val) { return !val.upload; });
            } else {
                for (var i in this.attachment_ids) {
                    if (this.attachment_ids[i].name == result.name && this.attachment_ids[i].upload) {
                        this.attachment_ids[i]={
                            'id': result.id,
                            'name': result.name,
                            'filename': "link",
                            'url': result.url,
                            'is_url': true
                        };
                    }
                }
            }
            
            
            this.display_attachments();
            console.log("AFTER DISPLAY");
            var $input = this.$('input.oe_attach_link');
            $input.after($input.clone(true)).remove();
            this.$(".oe_attachment_file").show();
        },
        


        
    });
    
    
    
/*
   ZALUPA_ROBERTA_KUKA.mail.ThreadComposeMessage = ZALUPA_ROBERTA_KUKA.mail.ThreadComposeMessage.extend({
        breakword: function(str){
            var out = '';
            if (!str) {
                return str;
            }
            for(var i = 0, len = str.length; i < len; i++){
                out += _.str.escapeHTML(str[i]) + '&#8203;';
            }
            return out;
        },
        get_attachment_url: function (session, message_id, attachment_id) {
            return session.url('/mail/download_attachment', {
                'model': 'mail.message',
                'id': message_id,
                'method': 'download_attachment',
                'attachment_id': attachment_id
            });
        },
        display_attachments: function () {
             console.log("DISPLAY");
            for (var l in this.attachment_ids) {
                var attach = this.attachment_ids[l];
                console.log(attach);
            //    if(attach.name){
             //   if (attach.name.substring("http://")&&!attach.formating) {                                      
               //         console.log("MY IF");
              //          attach.url=attach.name+"/";
             //   attach.formating = true;}}
             //   else
                if (!attach.formating) {
                    attach.url = this.get_attachment_url(ZALUPA_ROBERTA_KUKA, this.id, attach.id);
                    attach.name = this.breakword(attach.name || attach.filename);
                    attach.formating = true;
                }
            }
            this.$(".oe_msg_attachment_list").html( ZALUPA_ROBERTA_KUKA.web.qweb.render('mail.thread.message.attachments', {'widget': this}) );
        },
    
  });
    */
};


