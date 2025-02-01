odoo.define('mail_remote_desktop', function(require) {
    var core = require('web.core');
    var qweb = core.qweb;
    var _t = core._t;
    var Registry = require('web.field_registry');
    var BasicFields = require('web.basic_fields');
    var Dialog = require('web.Dialog');
     var rpc = require('web.rpc');

    var Chatter = require('mail.Chatter');
    var Discuss = require('mail.Discuss');

var JitsiDialog = Dialog.extend({
    dialog_title: _t("Remote desktop"),
    template: 'JitsiDialog',


    init: function (parent, parentID) {

        this.parentID = parentID;
        this.jitsi_room = 'Eurodoo' + parentID;
        this.parent = parent;

        this._super(parent, {
            title: _t("Remote desktop"),
            size: 'large',
            buttons: [{
                text: _t("Close"),
                close: true,
                classes: 'btn-primary',
                click: this.destroy.bind(this)
            }],
        });
    },

    start: function () {
        var self = this;
        rpc.query({
            route: '/domain/voip',
        }).then( data => {
            console.log('DATA DOMAIN');
            console.log(data.domain);
            if (data.domain)
                this.domain = data.domain;
            else
                this.domain = 'jitsi.ufanet.ru';


            this.$input = this.$('#jitsi');
            this.options = {
                roomName: this.jitsi_room,
                width: '100%',
                height: '100%',
                parentNode: this.$input[0]
            };
            this.api = new JitsiMeetExternalAPI(this.domain, this.options);


	         var message = {
	                    jitsi_room: this.jitsi_room,
	                    subtype_id: false,
	                    message_type: 'comment',
	                    content: `https://${this.domain}/${this.jitsi_room}`
	                };

	            this.parent._onPostMessage(message);

        });
        return this._super.apply(this, arguments);

    },

    destroy: function () {
        this.api.dispose();
        this._super.apply(this, arguments);
    },
});
    

    Discuss.include({
        events: _.extend({}, Discuss.prototype.events, {
            'click .remote-desktop': '_onOpenRemoteDesktop',
        }),

        _onOpenRemoteDesktop: function (ev) {
            new JitsiDialog(this, this._defaultThreadID.toString()).open();
        },
    })


});