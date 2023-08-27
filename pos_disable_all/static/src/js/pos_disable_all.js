odoo.define("pos_disable_all", function (require) {
  "use strict";
  var models = require("point_of_sale.models");

  models.load_fields("res.users", [
    "allow_payments",
    "allow_delete_order",
    "allow_discount",
    "allow_edit_price",
    "allow_decrease_amount",
    "allow_delete_order_line",
    "allow_create_order_line",
    "allow_refund",
    "allow_manual_customer_selecting",
    "allow_cash_in_out",
  ]);
  const components = {
    NumpadWidget: require("point_of_sale.NumpadWidget"),
    TicketScreen: require("point_of_sale.TicketScreen"),
  };
  const { patch } = require("web.utils");

  patch(components.TicketScreen.prototype, "ticket_disable", {
    hideDeleteButton(order) {
      if (!this.env.pos.user.allow_delete_order) return true;
      return order
        .get_paymentlines()
        .some(
          (payment) =>
            payment.is_electronic() && payment.get_payment_status() === "done",
        );
    },
  });

  patch(components.NumpadWidget.prototype, "pos_disable_all", {
    mounted() {
      if (this.env.pos.user.allow_cash_in_out) {
        $(".cash-move-button").removeClass("disable");
      } else {
        $(".cash-move-button").remove();
      }

      this.env.pos.on("change:cashier", () => {
        if (!this.hasPriceControlRights && this.props.activeMode === "price") {
          this.trigger("set-numpad-mode", { mode: "quantity" });
        }
      });

      if (this.env.pos.user.allow_manual_customer_selecting) {
        $(".set-customer").removeClass("disable");
      } else {
        $(".set-customer").addClass("disable");
      }

      if (this.env.pos.user.allow_refund) {
        $(".numpad-minus").removeClass("disable");
      } else {
        $(".numpad-minus").addClass("disable");
      }

      if (this.env.pos.user.allow_delete_order_line) {
        $(".numpad-backspace").removeClass("disable");
      } else {
        $(".numpad-backspace").addClass("disable");
      }

      if (this.env.pos.user.allow_payments) {
        $(".button.pay").removeClass("disable");
      } else {
        $(".button.pay").addClass("disable");
      }

      if (this.env.pos.user.allow_create_order_line) {
        $(".numpad").show();
        $(".rightpane").show();
      } else {
        $(".numpad").hide();
        $(".rightpane").hide();
      }

      if (this.env.pos.user.allow_decrease_amount) {
        $($(".numpad").find(".mode-button")[0]).removeClass("disable");
      } else {
        $($(".numpad").find(".mode-button")[0]).addClass("disable");
      }

      if (this.env.pos.user.allow_edit_price) {
        $($(".numpad").find(".mode-button")[2]).removeClass("disable");
      } else {
        $($(".numpad").find(".mode-button")[2]).addClass("disable");
      }

      if (this.env.pos.user.allow_discount) {
        $($(".numpad").find(".mode-button")[1]).removeClass("disable");
      } else {
        $($(".numpad").find(".mode-button")[1]).addClass("disable");
      }
    },
    changeMode(mode) {
      if (!this.env.pos.user.allow_decrease_amount && mode === "quantity") {
        return;
      }
      if (!this.hasPriceControlRights && mode === "price") {
        return;
      }
      if (!this.env.pos.user.allow_edit_price && mode === "price") return;
      if (!this.env.pos.user.allow_discount && mode === "discount") return;
      if (!this.hasManualDiscount && mode === "discount") {
        return;
      }
      this.trigger("set-numpad-mode", { mode });
    },
  });
});
