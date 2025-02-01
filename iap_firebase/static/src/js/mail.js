odoo.define('iap_firebase.mail', function(require) {
    "use strict";

    var core = require('web.core');
    var Discuss = require('mail.Discuss');
    var Thread = require('mail.model.Thread');
    var QWeb = core.qweb;
    var rpc = require('web.rpc');
    var _t = core._t;


    var Discuss = Discuss.include({
/*        init: function (parent, options) {
            this._super.apply(this, arguments);
            var self = this;
            var domain = [];
            domain.push(['key', '=', 'firebase_key']);
*//*            rpc.query({
                method: 'search_read',
                args: [domain, ['value']],
                model: 'ir.config_parameter'
            })
            .then(function (res){
                console.log(res)
            })*/

/*            if (!self.iap_firebase)
            this._rpc({
                args: [domain, ['value']],
                method: 'search_read',
                model: 'ir.config_parameter',

            })
            .then(function (res){
                console.log(res[0].value);
                self.iap_firebase = res[0].value;
            })*/

     //   },

/*        _onPostMessage: function (data) {
            console.log("Thread")
            console.log(this)
            this._super.apply(this, arguments);

        }*/
    });
    
/*    var Thread = Thread.include({
        
        _postMessage: function (data) {
            console.log("Thread")
            console.log(this._members)
            console.log(this)
            console.log(data)
            return this._super.apply(this, arguments);

        }
    });*/
/*            var self = this;
            $.ajax({
                url: 'https://fcm.googleapis.com/fcm/send',
                type: 'post',
                data: {
                    "notification": {
                        "title": "Notification Title",
                        "text": messageData.content
                    },
                    "project_id": "com.eurodoo",
                    "to":"the specific client-device-id"
                },
                headers: {
                    "Content-Type: application/json",   //If your header name has spaces or any other char not appropriate
                    "Authorization: key={"+ self.iap_firebase + "}"  //for object property name, use quoted notation shown in second
                },
                dataType: 'json',
                success: function (data) {
                    console.info(data);
                    console.log(data);
                }
            });*/



});
