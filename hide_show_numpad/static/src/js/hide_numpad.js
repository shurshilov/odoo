odoo.define('hide_show_numpad', function (require) {
    "use strict";

    const ProductScreen = require('point_of_sale.ProductScreen');
    const { useListener } = require('web.custom_hooks');
    const Registries = require("point_of_sale.Registries");


    const ProductScreenHideShowNumpad = (ProductScreen) =>
        class extends ProductScreen {
            clickHideShowNumpad (){
                var self = this;
                $(document.querySelector('.pads')).slideToggle(function () {
                    $(self).toggleClass('fa-caret-down fa-caret-up');
                    if($(this).is(':visible')){
                        $('.order-scroller').animate({scrollTop: $('.order-scroller').height()}, 500);
                    }
                });
            }
        }
    Registries.Component.extend(ProductScreen, ProductScreenHideShowNumpad);
    return ProductScreen;
});
