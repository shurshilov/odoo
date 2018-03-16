odoo.define('mail_reply.forward', function (require) {
"use strict";

var core = require('web.core');
var base_obj = require('mail_base.base');
var time = require('web.time');
var mythread = require('mail.ChatThread');

var ChatAction = core.action_registry.get('mail.chat.instant_messaging');
mythread.include({
	
	    events: {
        "click a": "on_click_redirect",
        "click img": "on_click_redirect",
        "click strong": "on_click_redirect",
        "click .o_thread_show_more": "on_click_show_more",
        "click .o_thread_message_needaction": function (event) {
            var message_id = $(event.currentTarget).data('message-id');
            this.trigger("mark_as_read", message_id);
        },
        "click .o_thread_message_star": function (event) {
            var message_id = $(event.currentTarget).data('message-id');
            this.trigger("toggle_star_status", message_id);
        },
        "click .o_thread_message_reply": function (event) {
            this.selected_id = $(event.currentTarget).data('message-id');
            this.$('.o_thread_message').removeClass('o_thread_selected_message');
            this.$('.o_thread_message[data-message-id=' + this.selected_id + ']')
                .addClass('o_thread_selected_message');
            this.trigger('select_message', this.selected_id);
            event.stopPropagation();
        },
		"click .o_thread_message_forward": function (event) {
            this.selected_id = $(event.currentTarget).data('message-id');
            this.$('.o_thread_message').removeClass('o_thread_selected_message');
            this.$('.o_thread_message[data-message-id=' + this.selected_id + ']')
                .addClass('o_thread_selected_message');
            //this.trigger('select_message', this.selected_id);
			this.select_message_forward(this.selected_id);
			
            event.stopPropagation();
        },
        "click .oe_mail_expand": function (event) {
            event.preventDefault();
            var $message = $(event.currentTarget).parents('.o_thread_message');
            $message.addClass('o_message_expanded');
            this.expanded_msg_ids.push($message.data('message-id'));
        },
        "click .o_thread_message": function (event) {
            $(event.currentTarget).toggleClass('o_thread_selected_message');
        },
        "click": function () {
            if (this.selected_id) {
                this.unselect();
                this.trigger('unselect_message');
            }
        },
    },
		select_message_forward: function(message_id) {
		var message = base_obj.chat_manager.get_message(message_id);
		var tmp = document.createElement("DIV");
		tmp.innerHTML =  message.body;
		var msg = "\n<br>   ---------------\n<br>   Fw from: " +
		 message.email_from +  "\n<br>   Fw date: " + new Date(message.date) + message.body;
		
        this.do_action({
            type: 'ir.actions.act_window',
            res_model: 'mail.compose.message',
            view_mode: 'form',
            view_type: 'form',
            views: [[false, 'form']],
            target: 'new',
            context: "{'subject': \'Fw: "+message.subject+"\','default_no_auto_thread': False, 'active_model': 'mail.message', 'body': \'"+msg+"\'}",
        });  

    },
	});
ChatAction.include({
	
    start: function() {
        var result = this._super.apply(this, arguments);

        var search_defaults = {};
        var context = this.action ? this.action.context : [];
        _.each(context, function (value, key) {
            var match = /^search_default_(.*)$/.exec(key);
            if (match) {
                search_defaults[match[1]] = value;
            }
        });
        this.searchview.defaults = search_defaults;
		this.$('.o_composer_input textarea').focus(function () {
					var input = this;
					setTimeout(function() {
						input.setSelectionRange(0, 0);
					}, 0);
				});
        var self = this;
        return $.when(result).done(function() {
            $('.oe_leftbar').toggle(false);
            self.searchview.do_search();
        });
    },/*
	select_message_forward: function(message_id) {
        this.do_action({
            type: 'ir.actions.act_window',
            res_model: 'mail.compose.message',
            view_mode: 'form',
            view_type: 'form',
            views: [[false, 'form']],
            target: 'new',
            context: "{'default_no_auto_thread': False, 'active_model': 'mail.message'}",
        });  
    },*/
    select_message: function(message_id) {
        this._super.apply(this, arguments);
        var message = base_obj.chat_manager.get_message(message_id);
        var subject = '';
        if (message.record_name){
            subject = "Re1: " + message.record_name+message.email_from;
        } else if (message.subject){
            subject = "Re: " + message.subject ; 
        }
		
		var tmp = document.createElement("DIV");
		var divNode = document.createElement("div");
		//tmp.innerHTML = "<p style=\"border-left: 2px solid #ccc; margin-left: 20px; padding-left: 10px;\">" + message.body + "</p>";
		tmp.innerHTML =  message.body;
	//return tmp.textContent || tmp.innerText || ""; moment(time.str_to_datetime(data.date))
		
		
	
		this.$('.o_composer_input textarea').val("\n   ---------------\n   Re from: " +
		 message.email_from +  "\n   Re date: " + new Date(message.date) + "\n   " + tmp.innerText.replace(/\n/g,"\n   "));

        this.extended_composer.set_subject(subject);
    },
    on_post_message: function(message){
        var self = this;
        var options = this.selected_message ? {} : {channel_id: this.channel.id};
		            message.subtype_id = false;
            message.no_auto_thread = false;
            message.message_type = 'email';
        if (this.selected_message) {
         //   message.subtype = 'mail.mt_comment';

         //   message.content_subtype = 'html';

            options.model = this.selected_message.model;
            options.res_id = this.selected_message.res_id;
            options.parent_id = this.selected_message.id;

			}
        base_obj.chat_manager
            .post_message(message, options)
            .then(function() {
                if (self.selected_message) {
                    self.render_snackbar('mail.chat.MessageSentSnackbar', {record_name: self.selected_message.subject}, 5000);
                    self.unselect_message();
                } else {
                    self.thread.scroll_to();
                }
            });
    }
});

});
