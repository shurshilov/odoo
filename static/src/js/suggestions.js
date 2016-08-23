openerp.mail_extension = function (session) {
	var mail = session.mail;
    mail.ThreadMessage = mail.ThreadMessage.extend({

    
        on_record_author_clicked: function  (event) {            
            var self = this;
            event.preventDefault();
            var partner_id = $(event.target).data('partner');
            
            var state = {
                'model': 'mypartner',
                'id': partner_id,
                'title': this.record_name
            };

           function getResults (result) {
                console.log(result); // to see which data come from server
                zopa = result;
                $("oe_mail_action_author").attr("id","4");
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
            session.webclient.action_manager.do_push_state(state);
            var model = new openerp.web.Model('my_mypartner');
            var aaa = model.call('sync_visitors',[partner_id,])
            .done(getResults).fail(getError);

        },
        


        
        
        
        
    });




};
