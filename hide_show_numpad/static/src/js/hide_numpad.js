
odoo.define('hide_show_numpad', function (require) {
    "use strict";
    const ProductScreen = require('point_of_sale.ProductScreen');
    const { patch } = require('web.utils');

    patch(ProductScreen.prototype, 'hide_show_numpad', {
        toogleNumpad() {
            $('.pads').slideToggle(() => {
                $('.numpad-toggle').toggleClass('fa-caret-down fa-caret-up');
                if ($(this).is(':visible'))
                    $('.order-scroller').animate({ scrollTop: $('.order-scroller').height() }, 500);
            });
        }
    })

});
