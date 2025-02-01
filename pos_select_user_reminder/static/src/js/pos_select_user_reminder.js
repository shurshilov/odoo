odoo.define('pos_select_user_reminder', function(require){
    "use strict";

    var screens = require('point_of_sale.screens');
    var ActionpadWidget = screens.ActionpadWidget;
    var gui = require('point_of_sale.gui');
    var _t  = require('web.core')._t;

screens.ActionpadWidget.include({
	    renderElement: function() {
        var self = this;
        this._super();
        this.$('.pay').click(function(){
            var order = self.pos.get_order();
            var has_valid_product_lot = _.every(order.orderlines.models, function(line){
                return line.has_valid_product_lot();
            });
            if(!has_valid_product_lot){
                self.gui.show_popup('confirm',{
                    'title': _t('Empty Serial/Lot Number'),
                    'body':  _t('One or more product(s) required serial/lot number.'),
                    confirm: function(){
                        self.gui.show_screen('payment');
                    },
                });
            }else{
                self.gui.show_screen('payment');
            }
            self.chrome.widget.username.click_username();
        });
        this.$('.set-customer').click(function(){
            self.gui.show_screen('clientlist');
        });
    }
/*	renderElement: function(){
		var self = this;
        this._super();
        $('.button.pay').on('click', function () {
            console.log(self)
            console.log(self.chrome.widget.username)
            self.chrome.widget.username.click_username();
            //$('.username').click();
            //self.gui.select_user({'required': true,});
        });
	}*/
})

/*screens.NumpadWidget.include({
    renderElement: function(){
        var self = this;
        this._super();
        $('.button.pay').on('click', function () {
            console.log(self)
            console.log(self.chrome.widget.username.click_username())
            console.log(self.chrome.widget.username)
            self.chrome.widget.username.click_username();
            //$('.username').click();
            //self.gui.select_user({'required': true,});
        });
    },
});*/
/*
gui.Gui.include({
 select_user: function(options){
        options = options || {};
        var self = this;
        var def  = new $.Deferred();

        var list = [];
        for (var i = 0; i < this.pos.users.length; i++) {
            var employer = this.pos.users[i];
            list.push({
                'label': employer.name,
                'item':  employer,
            });
        }

        this.show_popup('selection',{
            'title': options.title || _t('Select User'),
            list: list,
            confirm: function(employer){ def.resolve(employer); },
            cancel:  function(){ def.reject(); },
        });

    return def.then(function(employer){
            return self.ask_password(employer.pos_security_pin).then(function(){
                self.pos.employee = employer;
                self.pos.chrome.widget.username.renderElement();
                self.pos.set_cashier(self.pos.employee);
                //self.pos.maywork.resolve();
                return self.pos.employee;
            },
            function(){
                if(options.required) return self.select_user({'required': true,});
            });
        },
        function(){
            if(options.required) return self.select_user({'required': true,});
        });

    },
        ask_password: function(password) {
        var self = this;
        var ret = new $.Deferred();
        if (password) {
            this.show_popup('password',{
                'title': _t('Password ?'),
                confirm: function(pw) {
                    if (pw !== password) {
                        self.show_popup('error',_t('Incorrect Password'));
                        ret.reject();
                    } else {
                        ret.resolve();
                    }
                },
                cancel: function(){ ret.reject(); },
            });
        } else {
            ret.resolve();
        }
        return ret;
    },
});
*/




});
