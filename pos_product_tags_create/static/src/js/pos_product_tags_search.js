// Copyright (C) 2018 Artem Shurshilov <shurshilov.a@yandex.ru>
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
odoo.define('pos_product_tags_search.pos_extend', function (require) {
"use strict";

    var POS_models = require('point_of_sale.models');
    var POS_db = require('point_of_sale.DB');
    var ProductListWidget = require('point_of_sale.screens').ProductListWidget;
    var gui = require('point_of_sale.gui');
    var _t  = require('web.core')._t;
    var rpc = require('web.rpc');


ProductListWidget.include({
    init: function(parent, options) {
        var self = this;
        this._super(parent,options);
        this.click_product_handler = function(e){
	    if (e.target.classList.contains('edit_tags_product')){

		var id = Number($(e.target).data('product-id'));
	        self.gui.show_popup('textinput',{
    		    'title': _t('Please set new tag'),
            	    'value': '',
        	    'confirm': function(value) {
			if (!value)
			    return;
			rpc.query({
            		    model: 'product.template',
            		    method: 'create_from_ui_tag',
            		    args: [id, value],
        		})
        		.then(function(create){
            		    self.gui.show_popup('alert',{
                		'title': _t('Success'),
                		'body': create,
            		    });
			    self.show();

        		},function(err,ev){
	                    ev.preventDefault();
        		    var error_body = _t('Your Internet connection is probably down.');
	                    if (err.data) {
        		        var except = err.data;
	                        error_body = except.arguments && except.arguments[0] || except.message || error_body;
        		    }
	                    self.gui.show_popup('error',{
        		        'title': _t('Error: Could not Save Changes'),
	                        'body': error_body,
        		    });
			    // contents.on('click','.button.save',function(){ self.save_client_details(partner); });
        		});
		    }
    		});

		return;
	    }
            var product = self.pos.db.get_product_by_id(this.dataset.productId);
            options.click_product_action(product);
        };
    },

});

POS_db.include({
    _product_search_string: function(product){
        var str = product.display_name;
        if (product.barcode) {
            str += '|' + product.barcode;
        }
        if (product.default_code) {
            str += '|' + product.default_code;
        }
        if (product.description) {
            str += '|' + product.description;
        }
        //MY
        if (product.tag_ids_name) {
            str += '|' + product.tag_ids_name;
        }
        if (product.description_sale) {
            str += '|' + product.description_sale;
        }
        str  = product.id + ':' + str.replace(/:/g,'') + '\n';
        return str;
    },
});

var exports = {};
exports.Product = Backbone.Model.extend({
    initialize: function(attr, options){
        _.extend(this, options);
    },

    // Port of get_product_price on product.pricelist.
    //
    // Anything related to UOM can be ignored, the POS will always use
    // the default UOM set on the product and the user cannot change
    // it.
    //
    // Pricelist items do not have to be sorted. All
    // product.pricelist.item records are loaded with a search_read
    // and were automatically sorted based on their _order by the
    // ORM. After that they are added in this order to the pricelists.
    get_price: function(pricelist, quantity){
        var self = this;
        var date = moment().startOf('day');

        var category_ids = [];
        var category = this.categ;
        while (category) {
            category_ids.push(category.id);
            category = category.parent;
        }

        var pricelist_items = _.filter(pricelist.items, function (item) {
            return (! item.product_tmpl_id || item.product_tmpl_id[0] === self.product_tmpl_id) &&
                   (! item.product_id || item.product_id[0] === self.id) &&
                   (! item.categ_id || _.contains(category_ids, item.categ_id[0])) &&
                   (! item.date_start || moment(item.date_start).isSameOrBefore(date)) &&
                   (! item.date_end || moment(item.date_end).isSameOrAfter(date));
        });

        var price = self.lst_price;
        _.find(pricelist_items, function (rule) {
            if (rule.min_quantity && quantity < rule.min_quantity) {
                return false;
            }

            if (rule.base === 'pricelist') {
                price = self.get_price(rule.base_pricelist, quantity);
            } else if (rule.base === 'standard_price') {
                price = self.standard_price;
            }

            if (rule.compute_price === 'fixed') {
                price = rule.fixed_price;
                return true;
            } else if (rule.compute_price === 'percentage') {
                price = price - (price * (rule.percent_price / 100));
                return true;
            } else {
                var price_limit = price;
                price = price - (price * (rule.price_discount / 100));
                if (rule.price_round) {
                    price = round_pr(price, rule.price_round);
                }
                if (rule.price_surcharge) {
                    price += rule.price_surcharge;
                }
                if (rule.price_min_margin) {
                    price = Math.max(price, price_limit + rule.price_min_margin);
                }
                if (rule.price_max_margin) {
                    price = Math.min(price, price_limit + rule.price_max_margin);
                }
                return true;
            }

            return false;
        });

        // This return value has to be rounded with round_di before
        // being used further. Note that this cannot happen here,
        // because it would cause inconsistencies with the backend for
        // pricelist that have base == 'pricelist'.
        return price;
    },
});

POS_models.load_models({
   model:  'product.product',
        // todo remove list_price in master, it is unused
        fields: ['display_name', 'list_price', 'lst_price', 'standard_price', 'categ_id', 'pos_categ_id', 'taxes_id',
                 'barcode', 'default_code', 'to_weight', 'uom_id', 'description_sale', 'description',
                 'product_tmpl_id','tracking','tag_ids_name'],
        order:  _.map(['sequence','default_code','name'], function (name) { return {name: name}; }),
        domain: [['sale_ok','=',true],['available_in_pos','=',true]],
        context: function(self){ return { display_default_code: false }; },
        loaded: function(self, products){
                self.db.add_products(_.map(products, function (product) {
                //console.log(product.tag_ids_name)
                product.categ = _.findWhere(self.product_categories, {'id': product.categ_id[0]});
                return new exports.Product({}, product);
            }));
        },
});

 



});
