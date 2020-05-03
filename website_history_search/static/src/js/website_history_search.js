odoo.define('odoo_website_search_suggestion.odoo_website_search_suggestion', function(require) {
    "use strict";

    var core = require('web.core');
    var utils = require('web.utils');
    var qweb = core.qweb;
    var _t = core._t;

    var publicWidget = require('web.public.widget');
    require('website_sale.website_sale');

publicWidget.registry.productsSearchBar.include({
    events: _.extend({}, publicWidget.registry.productsSearchBar.prototype.events, {
        'click .search-query': '_onClick',
        }),
    
    _onClick: function (ev) {
        if (!this.limit) {
            return;
        }

        if (utils.get_cookie('history_search')) {
            var history = utils.get_cookie('history_search').split('|');
            var res = {products: []}
            for (let i=0; i < history.length; i++){
                var $this = $(ev.delegateTarget);
                ev.preventDefault();
                var oldurl = $this.attr('action');
                oldurl += (oldurl.indexOf("?")===-1) ? "?" : "";
                var search = history[i];
                res['products'].push({
                        name: history[i],
                        website_url: oldurl + '&search=' + encodeURIComponent(search),
                        price: '<span class="fa fa-times o_history_delete_cross" data-name="'+history[i]+'"></span>'
                })
            }
            this.displayImage = false;
            this._render(res);
        }
    },
    
    _render: function (res) {
        var self = this;
        this._super.apply(this, arguments);

        if (!this.displayImage){
            $('.o_history_delete_cross').click(function(e){ // задаем функцию при нажатиии на элемент <button>
                e.preventDefault();
                console.log(e);
                var name_del = $(e.target).data('name');
                var history = utils.get_cookie('history_search').split('|');
                console.log(history);
                var res = "";
                for (let i=0; i < history.length; i++){
                    if (history[i] !== name_del){
                        if (i !== history.length -1)
                            res +=history [i] + '|';
                        else
                            res +=history [i];
                    }
                }
                utils.set_cookie('history_search', res);
                console.log(res);
                $('.search-query').click();
            });
            this.displayImage = true;
        }
    },
})


publicWidget.registry.WebsiteSale.include({
    _onSubmitSaleSearch: function (ev) {
       if (!this.$('.dropdown_sorty_by').length) {
            return;
        }
        var $this = $(ev.currentTarget);
        if (!ev.isDefaultPrevented() && !$this.is(".disabled")) {
            ev.preventDefault();
            var oldurl = $this.attr('action');
            oldurl += (oldurl.indexOf("?")===-1) ? "?" : "";
            var search = $this.find('input.search-query');
            var get_data = utils.get_cookie('history_search');
            if (get_data)
                utils.set_cookie('history_search', search.val() + '|' + get_data);
            else
                utils.set_cookie('history_search', search.val());
            window.location = oldurl + '&' + search.attr('name') + '=' + encodeURIComponent(search.val());

        }
        
    },
})


});
