openerp.mail_extension = function (session) {
	var mail = session.mail;
    mail.ThreadMessage = mail.ThreadMessage.extend({

        on_record_author_clicked: function  (event) {
            event.preventDefault();
            var partner_id = $(event.target).data('partner');
			//alert($(event.target).data);
            var state = {
                'model': 'mypartner',
                'id': partner_id,
                'title': this.record_name
            };
            session.webclient.action_manager.do_push_state(state);
            var action = {
                type:'ir.actions.act_window',
                view_type: 'form',
                view_mode: 'form',
                res_model: 'my_mypartner',
                views: [[false, 'form']],
                res_id: 1,
				context: {'partner_id': partner_id},
            }
            this.do_action(action);
        },
    });




};
