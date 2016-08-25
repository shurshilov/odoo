openerp.mail_extension = function (ZALUPA_ROBERTA_KUKA) {
    
    ZALUPA_ROBERTA_KUKA.web.WebClient.include({
        init: function(parent, client_options) {
            this._super(parent, client_options);
            this.set('title_part', {"zopenerp": "MyModule"});
        },
        set_title: function(title) {
          title = _.str.clean(title);
          var sep = _.isEmpty(title) ? '' : ' - ';
          document.title = title + sep + 'MyModule';
        },
    });

	var mail = ZALUPA_ROBERTA_KUKA.mail;
    mail.ThreadMessage = mail.ThreadMessage.extend({   
    
        //extend function ADD on_click action
        bind_events: function () {
            var self = this;
            self._super(self);
            self.$('.oe_msg_icon').on('click', self.on_record_author_clicked);
        },
    
        on_record_author_clicked: function  (event) {            
            var self = this;
            event.preventDefault();
            
            //if click link get id from data
            var partner_id = $(event.target).data('partner');
            
            //if click icon get id from url of icon
            if (!partner_id){
                var url = $(event.target).context.src;
                partner_id = url.substring(url.lastIndexOf('id=') + 3).match(/\d+/);        
                console.log(partner_id[0]);
            }
            
            var state = {
                'model': 'my_mypartner',
                'id': this.partner_id,
                'title': this.record_name
            };

           function getResults (result) {
            var action = {
                type:'ir.actions.act_window',
                view_type: 'form',
                view_mode: 'form',
                res_model: 'my_mypartner',
                views: [[false, 'form']],
                res_id: result[0],
				context: {'partner_id': partner_id},
            }
                self.do_action(action);
                return result;
            }
            function getError (result) {
               // console.log(result); // to see which data come from server
            }
            ZALUPA_ROBERTA_KUKA.webclient.action_manager.do_push_state(state);
            var model = new openerp.web.Model('my_mypartner');
            var aaa = model.call('sync_visitors',[partner_id,])
            .done(getResults).fail(getError);

        },
        


        
        
        
        
    });




};


           /* have unknown names -> call message_get_partner_info_from_emails to try to find partner_id
            var find_done = $.Deferred();
            if (names_to_find.length > 0) {
                find_done = self.parent_thread.ds_thread._model.call('message_partner_info_from_emails', [this.context.default_res_id, names_to_find]);
            }
            else {
                find_done.resolve([]);
            }
*/