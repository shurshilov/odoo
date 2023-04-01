odoo.define('pos_disable_all', function(require){
    "use strict";
    var models = require('point_of_sale.models');

    models.load_fields("res.users", ['allow_payments','allow_delete_order','allow_discount','allow_edit_price','allow_decrease_amount', 'allow_delete_order_line','allow_create_order_line','allow_refund','allow_manual_customer_selecting']);
const components = {
    NumpadWidget: require('point_of_sale.NumpadWidget'),
    TicketScreen: require('point_of_sale.TicketScreen'),
};
const { patch } = require('web.utils');



patch(components.TicketScreen, 'ticket_disable', {
    hideDeleteButton(order) {
        if (!this.env.pos.user.allow_delete_order)
            return true
        return order
            .get_paymentlines()
            .some((payment) => payment.is_electronic() && payment.get_payment_status() === 'done');
    }
});

patch(components.NumpadWidget, 'pos_disable_all', {
        mounted() {
            this.env.pos.on('change:cashier', () => {
                if (!this.hasPriceControlRights && this.props.activeMode === 'price') {
                    this.trigger('set-numpad-mode', { mode: 'quantity' });
                }
            });

            if (this.env.pos.user.allow_manual_customer_selecting) {
                $('.set-customer').removeClass('disable');
            } else {
                $('.set-customer').addClass('disable');
            }

            if (this.env.pos.user.allow_refund) {
                $('.numpad-minus').removeClass('disable');
            }else{
                $('.numpad-minus').addClass('disable');
            }

            if (this.env.pos.user.allow_delete_order_line) {
                $('.numpad-backspace').removeClass('disable');
            } else {
                $('.numpad-backspace').addClass('disable');
            }

            if (this.env.pos.user.allow_payments) {
                $('.button.pay').removeClass('disable');
            }else{
                $('.button.pay').addClass('disable');
            }

            if (this.env.pos.user.allow_create_order_line) {
                $('.numpad').show();
                $('.rightpane').show();
            }else{
                $('.numpad').hide();
                $('.rightpane').hide();
            }

            if (this.env.pos.user.allow_decrease_amount) {
                $($('.numpad').find('.mode-button')[0]).removeClass('disable');
            }else{
                $($('.numpad').find('.mode-button')[0]).addClass('disable');
            }

            if (this.env.pos.user.allow_edit_price) {
                $($('.numpad').find('.mode-button')[2]).removeClass('disable');
            }else{
                $($('.numpad').find('.mode-button')[2]).addClass('disable');
            }

            if (this.env.pos.user.allow_discount) {
                $($('.numpad').find('.mode-button')[1]).removeClass('disable');
            }else{
                $($('.numpad').find('.mode-button')[1]).addClass('disable');
            }
        },
        changeMode(mode) {
            if (!this.env.pos.user.allow_decrease_amount  && mode === 'quantity') {
                return;
            }
            if (!this.hasPriceControlRights && mode === 'price') {
                return;
            }
            if (!this.env.pos.user.allow_edit_price && mode === 'price')
               return;
            if (!this.env.pos.user.allow_discount && mode === 'discount')
               return;
            if (!this.hasManualDiscount && mode === 'discount') {
                return;
            }
            this.trigger('set-numpad-mode', { mode });
        }

})


/*

    var chrome = require('point_of_sale.chrome');
    var screens = require('point_of_sale.screens');
    var models = require('point_of_sale.models');
    var PosBaseWidget = require('point_of_sale.BaseWidget');

    models.load_fields("res.users", ['allow_payments','allow_delete_order','allow_discount','allow_edit_price','allow_decrease_amount',
     'allow_delete_order_line','allow_create_order_line','allow_refund','allow_manual_customer_selecting']);

    chrome.Chrome.include({
        init: function(){
            this._super.apply(this, arguments);
            this.pos.bind('change:selectedOrder', this.check_allow_delete_order, this);
            this.pos.bind('change:cashier', this.check_allow_delete_order, this);
        },
        check_allow_delete_order: function(){
            var user = this.pos.user;
            var order = this.pos.get_order();
            if (user) {
                if (!user.allow_delete_order){ //&& order.orderlines.length > 0) {
                    $('.deleteorder-button').addClass('disable');
                } else {
                    $('.deleteorder-button').removeClass('disable');
                }
            }
        },
        loading_hide: function(){
            this._super();
            //extra checks on init
            this.check_allow_delete_order();
        }
    });
    chrome.OrderSelectorWidget.include({
        renderElement: function(){
            this._super();
            this.chrome.check_allow_delete_order();
        }
    });

    screens.OrderWidget.include({
        bind_order_events: function(){
            this._super();
            var self = this;
            var order = this.pos.get('selectedOrder');
            order.orderlines.bind('add remove', this.chrome.check_allow_delete_order, this.chrome);
            this.pos.bind('change:cashier', function(){
                self.check_numpad_access();
            });
        },
        orderline_change: function(line) {
            this._super(line);
            var user = this.pos.user;
            if (line && line.quantity <= 0) {
                if (user.allow_delete_order_line) {
                    $('.numpad-backspace').removeClass('disable');
                } else {
                    $('.numpad-backspace').addClass('disable');
                }
            } else {
                $('.numpad-backspace').removeClass('disable');
            }
            this.check_numpad_access(line);
        },
        click_line: function(orderline, event) {
            this._super(orderline, event);
            this.check_numpad_access(orderline);
        },
        renderElement:function(scrollbottom){
            this._super(scrollbottom);
            this.check_numpad_access();
        },
        check_numpad_access: function(line) {
            var order = this.pos.get_order();
            if (order) {
                line = line || order.get_selected_orderline();
                var user = this.pos.cashier || this.pos.user;
                var state = this.getParent().numpad.state;
                if (!line) {
                    $('.numpad').find('.numpad-backspace').removeClass('disable');
                    $('.numpad').find("[data-mode='quantity']").removeClass('disable');
                    return false;
                }

                if (user.allow_decrease_amount) {
                    // allow all buttons
                    if ($('.numpad').find("[data-mode='quantity']").hasClass('disable')) {
                        $('.numpad').find("[data-mode='quantity']").removeClass('disable');
                        state.changeMode('quantity');
                    }
                    if (user.allow_delete_order_line) {
                        $('.numpad').find('.numpad-backspace').removeClass('disable');
                    }
                } else {
                    // disable the backspace button of numpad
                    $('.pads .numpad').find('.numpad-backspace').addClass('disable');
                }
            }
        },
        orderline_change_line: function(line) {
            this._super(line);
            var user = this.pos.cashier || this.pos.user;
            var order = this.pos.get_order();
            if (order && !user.allow_decrease_amount) {
                // disable the backspace button of numpad
                $('.pads .numpad').find('.numpad-backspace').addClass('disable');
            }
        }
    });

    // Here regular binding (in init) do not work for some reasons. We got to put binding method in renderElement.
    screens.ProductScreenWidget.include({
        start: function () {
            this._super();
            this.checkPayAllowed();
            this.checkCreateOrderLine();
            this.checkDiscountButton();
        },
        renderElement: function () {
            this._super();
            this.pos.bind('change:cashier', this.checkPayAllowed, this);
            this.pos.bind('change:cashier', this.checkCreateOrderLine, this);
            this.pos.bind('change:cashier', this.checkDiscountButton, this);
        },
        checkCreateOrderLine: function () {
            var user = this.pos.user;
            if (user.allow_create_order_line) {
                $('.numpad').show();
                $('.rightpane').show();
            }else{
                $('.numpad').hide();
                $('.rightpane').hide();
            }
        },
        checkPayAllowed: function () {
            var user = this.pos.user;
            if (user.allow_payments) {
                //this.actionpad.$('.pay').removeClass('disable');
                this.$('.button.pay').removeClass('disable');
            }else{
                //this.actionpad.$('.button.pay').addClass('disable');
                this.$('.button.pay').addClass('disable');
            }
        },
        checkDiscountButton: function() {
            var user = this.pos.user;
            if (user.allow_discount) {
                $('.control-button.js_discount').removeClass('disable');
            }else{
                $('.control-button.js_discount').addClass('disable');
            }
        },
        show: function(reset){
            this._super(reset);
            if (reset) {
                this.order_widget.check_numpad_access();
            }
        }
    });
    screens.ScreenWidget.include({
        renderElement: function () {
            this._super();
            var user = this.pos.user;
            if (user.allow_payments) {
                this.$('.button.pay').removeClass('disable');
            }else{
                this.$('.button.pay').addClass('disable');
            }
            if (user.allow_create_order_line) {
                $('.numpad').show();
                $('.rightpane').show();
            }else{
                $('.numpad').hide();
                $('.rightpane').hide();
            }
        }
    });
    screens.ActionpadWidget.include({
        init: function(parent, options) {
            var self = this;
            this._super(parent, options);
            this.pos.bind('change:cashier', this.checkManualCustomerSelecting, this);
        },
        checkManualCustomerSelecting: function() {
            var user = this.pos.user;
            if (user.allow_manual_customer_selecting) {
                this.$('.set-customer').removeClass('disable');
            } else {
                this.$('.set-customer').addClass('disable');
            }
        },
        renderElement: function () {
            this._super();
            var user = this.pos.user;
            if (user.allow_payments) {
                this.$('.button.pay').removeClass('disable');
            } else{
                this.$('.button.pay').addClass('disable');
            }
            this.checkManualCustomerSelecting();
        }
    });
    screens.PaymentScreenWidget.include({
        init: function(parent, options) {
            var self = this;
            this._super(parent, options);
            this.pos.bind('change:cashier', this.checkManualCustomerSelecting, this);
        },
        checkManualCustomerSelecting: function() {
            var user = this.pos.user;
            if (user.allow_manual_customer_selecting) {
                this.$('.js_set_customer').removeClass('disable');
            } else {
                this.$('.js_set_customer').addClass('disable');
            }
        },
        renderElement: function(){
            this._super();
            this.checkManualCustomerSelecting();
        }
    });
    screens.NumpadWidget.include({
        init: function () {
            this._super.apply(this, arguments);
            this.pos.bind('change:cashier', this.check_access, this);
        },
        renderElement: function(){
            this._super();
            this.check_access();
        },
        check_access: function(){
            var user = this.pos.user;
            var order = this.pos.get_order();
            var orderline = false;
            if (order) {
                orderline = order.get_selected_orderline();
            }
            if (user.allow_discount) {
                this.$el.find("[data-mode='discount']").removeClass('disable');
            }else{
                this.$el.find("[data-mode='discount']").addClass('disable');
            }
            if (user.allow_edit_price) {
                this.$el.find("[data-mode='price']").removeClass('disable');
            }else{
                this.$el.find("[data-mode='price']").addClass('disable');
            }
            if (user.allow_refund) {
                this.$el.find('.numpad-minus').removeClass('disable');
            }else{
                this.$el.find('.numpad-minus').addClass('disable');
            }
            if (orderline && orderline.quantity <= 0) {
                if (user.allow_delete_order_line) {
                    this.$el.find('.numpad-backspace').removeClass('disable');
                } else{
                    this.$el.find('.numpad-backspace').addClass('disable');
                }
            }
        }
    });

    return screens;*/
});
