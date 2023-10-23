/*  License MIT (https://opensource.org/licenses/MIT).
    Copyright 2020 Shurshilov Artem <shurshilov.a@yandex.ru> */

odoo.define("website_sale_available", function(require) {
    "use strict";

var publicWidget = require('web.public.widget');
require('website_sale.website_sale');
publicWidget.registry.WebsiteSale.include({
       start: function () {
            var res= this._super.apply(this, arguments);
            var disabling = $('#cart_products').find('tr.warning input').length;
            $('a[href^="/shop/checkout"]').toggleClass('disabled', !!disabling);
            return res;
    },
})

});
