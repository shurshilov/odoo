odoo.define('point_of_sale.ChatButton', function (require) {
    'use strict';

    const PosComponent = require('point_of_sale.PosComponent');
    const Registries = require('point_of_sale.Registries');

    class ChatButton extends PosComponent {
        _willDelete() {
            if (this.env.services['bus_service']) {
                this.env.services['bus_service'].off('notification');
                this.env.services['bus_service'].stopPolling();
            }
            return super._willDelete(...arguments);
        }
        sleep (ms) {
            return new Promise(resolve => setTimeout(resolve, ms));
        }
        print (ms) {
            console.log(ms);
        }
        async onClick() {
            
            await this.env.pos.do_action({
                type: "ir.actions.client",
                name: 'Discuss',
                tag: 'mail.widgets.discuss',
                res_model: 'mail.channel',
                params: {
                    'default_active_id': 'mail.box_inbox' 
                },
                target: 'new',
                // size: 'extra-large',
                dialogClass: 'o_web_client',
                fullscreen: true,
            })
            // await this.sleep(100)
            // this.env.services.messaging.refreshIsNotificationPermissionDefault();
            this.env.services.bus_service.onNotification(null, notifs => this.print(notifs));
            this.env.services.bus_service.startPolling()
            // this.env.bus.on("WEB_CLIENT_READY", null, async () => {
            //     console.log("START polling")
            //      this.env.services.bus_service.startPolling()
            // });
            
            $('.modal-dialog.modal-lg').css('position','relative')
            $('.modal-dialog.modal-lg').css('width','65%')
            $('.modal-dialog.modal-lg').css('height','95%')
            $('.o_debug_manager').hide()
            // $('.o_Discuss_content').addClass('o_Discuss_content_modal').removeClass('o_Discuss_content');
            $('.o_widget_Discuss').height($('.modal-dialog').height()*0.80)
            $('.modal-footer').hide()
        }

    }
    ChatButton.template = 'ChatButton';

    Registries.Component.add(ChatButton);

    return ChatButton;
});
