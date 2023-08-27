odoo.define("faceid.FaceId", function (require) {
  "use strict";

  var AbstractAction = require("web.AbstractAction");
  /*var ReconciliationModel = require('account.ReconciliationModel');
var ReconciliationRenderer = require('account.ReconciliationRenderer');
var ControlPanelMixin = require('web.ControlPanelMixin');*/
  var Widget = require("web.Widget");
  var Model = require("web.rpc");
  var core = require("web.core");
  var _t = core._t;
  var Context = require("web.Context");

  /**
   * Widget used as action for 'account.move.line' and 'res.partner' for the
   * manual reconciliation and mark data as reconciliate
   */
  var FaceId = AbstractAction.extend({
    updateImage: function (result) {
      console.log("1111");
    },

    start: function (parent) {
      var self = this;
      this._super(parent);
      alert("WORK!");
      console.log(this);
      var updateImage = function () {
        self.updateImage();
      };
      var url = new URL(self.el.baseURI);
      var id = Number(url.hash.split("&")[1].split("=")[1]);
      //console.log(Number(url.hash.split('&')[1].split('=')[1]))
      console.log(id);
      /*        self._rpc({
                    model: 'ir.model.data',
                    method: 'xmlid_to_res_id',
                    kwargs: {xmlid: 'sale.sale_product_configurator_view_form'},
                }).then(function (res_id) {*/
      this.do_action(
        {
          type: "ir.actions.act_window",
          res_model: "faceid.source",
          view_mode: "tree,form",
          view_type: "form",
          res_id: id,
          name: "Source form",
          views: [[false, "form"]],
          //views: [[false, 'list'],[false, 'form']],
          target: "current",
          /*        context: {
                        //'search_default_employee_id': [self.employee_data.uid],
                        'search_default_month': true,
                        },
                domain: ['|','|',['user_id', '=', self.employee_data.uid],
                ['employee_id.department_id.manager_id.user_id', '=', self.employee_data.uid],
                ['project_id.user_id','in',[self.employee_data.uid]]],*/
        },
        {
          //on_reverse_breadcrumb: function(){ return self.reload();},
          on_close: updateImage,
        },
      );
      //self.reload();
      console.log(this);
    },
  });

  core.action_registry.add("faceid", FaceId);

  return {
    FaceId: FaceId,
  };
});
