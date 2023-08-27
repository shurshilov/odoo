odoo.define("point_of_sale.ChatButton", function (require) {
  "use strict";

  const PosComponent = require("point_of_sale.PosComponent");
  const Registries = require("point_of_sale.Registries");

  class ChatButton extends PosComponent {
    sleep(ms) {
      return new Promise((resolve) => setTimeout(resolve, ms));
    }
    print(ms) {
      console.log(ms);
    }
    async onClick() {
      await this.env.pos.do_action({
        type: "ir.actions.client",
        name: "Discuss",
        tag: "mail.widgets.discuss",
        res_model: "mail.channel",
        params: {
          default_active_id: "mail.box_inbox",
        },
        target: "new",
        // size: 'extra-large',
        dialogClass: "o_web_client",
        fullscreen: true,
      });
      await this.sleep(100);
      this.env.services.bus_service.onNotification(null, (notifs) =>
        this.print(notifs),
      );
      this.env.services.bus_service.startPolling();
      $(".o_Discuss_content")
        .addClass("o_Discuss_content_modal")
        .removeClass("o_Discuss_content");
      $(".o_widget_Discuss").height($(".modal-dialog").height() * 0.8);
      $(".modal-footer").hide();
    }
  }
  ChatButton.template = "ChatButton";

  Registries.Component.add(ChatButton);

  return ChatButton;
});
