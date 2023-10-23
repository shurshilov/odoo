//Copyright 2020 Shurshilov Artem <shurshilov.a@yandex.ru>
odoo.define("website_swipe_images", function(require) {
    "use strict";
//var sAnimations = require('website.content.snippets.animation');
var publicWidget = require('web.public.widget');
require('website_sale.website_sale');
//sAnimations.registry.WebsiteSale.include({
publicWidget.registry.WebsiteSale.include({
        _updateProductImage: function ($productContainer, productId, productTemplateId, new_carousel, isCombinationPossible) {
            if($("#swipe_product").length)
                $(".carousel-inner").brazzersCarousel().closest(".brazzers-daddy").find(".hide_brazzers").css('display','contents');
            else
                this._super.apply(this, arguments);
        }

    });

$(document).ready(function(){
    if($("#swipe_products_item").length)
        // odoo  bug fix
        $(".carousel-inner").brazzersCarousel().closest(".brazzers-daddy").find(".hide_brazzers").css('display','contents');
});

});
