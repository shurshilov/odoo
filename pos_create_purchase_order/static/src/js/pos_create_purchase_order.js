odoo.define('pos_create_purchase_order.PosCreatePurchase', function(require) {
    "use strict";

    let core = require('web.core');
    const PosComponent = require('point_of_sale.PosComponent');
    const Registries = require('point_of_sale.Registries');
    let _t = core._t;

    class PosCreatePurchase extends PosComponent {       
        createPurchaseOrder (){
            let self = this;
            let currentOrder = self.env.pos.get_order();
			let partner_id = currentOrder.get_client();
			let orderlines = currentOrder.orderlines;
			let user_id = self.env.pos.get_cashier().user_id[0];

			if (!partner_id){
				self.showPopup('ErrorPopup', {
					'title': this.env._t('Empty customer'),
					'body': this.env._t('Please select customer'),
				});
				return;
			}
			partner_id = partner_id.id;

			if (orderlines.length === 0) {
				self.showPopup('ErrorPopup', {
					'title': this.env._t('Empty order'),
					'body': this.env._t('Products list empty, please adds any product'),
				});
				return;
			}

			let product_list = [];
			for (let i = 0; i < orderlines.length; i++) {
				let product_item = {
					'id': orderlines.models[i].product.id,
					'quantity': orderlines.models[i].quantity,
					'uom_id': orderlines.models[i].product.uom_id[0],
					'price': orderlines.models[i].price,
					'discount': orderlines.models[i].discount,
				};
				
				product_list.push({'product': product_item });
			}
			
			self.env.pos.rpc({
				model: 'purchase.order',
				method: 'create_purchase_order',
				args: [partner_id, partner_id, product_list, user_id],
			
			}).then( () => {
				self.showPopup('ConfirmPopup', {
					'title': self.env._t('Confirm'),
					'body': self.env._t('Sale Order Created'),
				});
				self.env.pos.delete_current_order();
			});
            
        }

    };
    PosCreatePurchase.template = 'PosCreatePurchase';
    Registries.Component.add(PosCreatePurchase);
    return PosCreatePurchase;
});
