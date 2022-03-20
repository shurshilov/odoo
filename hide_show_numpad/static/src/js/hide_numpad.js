odoo.define('hide_show_numpad', function (require) {
    "use strict";
    var screens = require('point_of_sale.screens');

    screens.NumpadWidget.include({
        renderElement: function () {
            this._super();
            $('.numpad-toggle').on('click', function () {
                var self = this;
                $(this).parent().siblings('.numpad-container').slideToggle(function () {
                    $(self).toggleClass('fa-caret-down fa-caret-up');
                    if($(this).is(':visible')){
                        $('.order-scroller').animate({scrollTop: $('.order-scroller').height()}, 500);
                    }
                });
            });
        }
    });
});
