//  Copyright 2021 Artem Shurshilov
//  Odoo Proprietary License v1.0

//  This software and associated files (the "Software") may only be used (executed,
//  modified, executed after modifications) if you have purchased a valid license
//  from the authors, typically via Odoo Apps, or if you have received a written
//  agreement from the authors of the Software (see the COPYRIGHT file).

//  You may develop Odoo modules that use the Software as a library (typically
//  by depending on it, importing it and using its resources), but without copying
//  any source code or material from the Software. You may distribute those
//  modules under the license of your choice, provided that this license is
//  compatible with the terms of the Odoo Proprietary License (For example:
//  LGPL, MIT, or proprietary licenses similar to this one).

//  It is forbidden to publish, distribute, sublicense, or sell copies of the Software
//  or modified copies of the Software.

//  The above copyright notice and this permission notice must be included in all
//  copies or substantial portions of the Software.

//  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
//  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
//  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
//  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
//  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
//  ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
//  DEALINGS IN THE SOFTWARE.


odoo.define('view_online_form', function (require) {
    "use strict";

    var core = require('web.core');
    var FormRenderer = require('web.FormRenderer');
    var _t = core._t;

    FormRenderer.include({
        end_count: 100,
        start_count: 0,
        view_online_form_on: true,
        update_timer: 5,
        colors: ["#3CC157", "#2AA7FF", "#1B1B1B", "#FCBC0F", "#F85F36"],
        // отправляем всем пользователям какую форму мы смотрим
        _view_online_form_channel: function () {
            return `view.online.form_${this.state.model}_${this.state.data.id}`
        },
        on_detach_callback: function () {
            this.view_online_form_on = false;
            this._tik_stop();
            this._sendMessage(0);
            return this._super.apply(this, arguments);
        },
        on_attach_callback: function () {
            this.view_online_form_on = true;
            this.start_count = 0;
            this._sendStatusOnlineViewForm();
            this._tik();
            return this._super.apply(this, arguments);
        },
        async _sendMessage(message){
            if (this.view_online_form_on && this.state && this.state.data && this.state.data.id) {
                let params = {
                    channel: this._view_online_form_channel(),
                    res_id: this.state.data.id,
                    uid: this.state.context.uid,
                    message: message
                }
                return this._rpc({
                    route: '/longpolling/send/viewonline',
                    params: params
                }, { shadow: true }).then((items) => {
                    if (message == 0) {
                        console.log('I am died :>> ');
                    } else {
                        this._renderUsersOnline(items)
                    }
                });
            }
        },
        _sendStatusOnlineViewForm: async function () {
            this.start_count += 1;
            // class Message(Enum):
            //     READ = 1
            //     ALIVE_READ = 2
            //     EDIT = 3
            //     ALIVE_EDIT = 4
            //     DIED = 0
            var message = 0;
            if (this.mode == 'readonly') {
                message = this.start_count > 1 ? 2 : 1
            } else {
                message = this.start_count > 1 ? 4 : 3
            }
            await this._sendMessage(message);
        },
        _tik: async function () {
            await this._sendStatusOnlineViewForm();
            this.timer = setTimeout(async () => {
                await this._tik();
            }, this.update_timer * 1000);

        },
        _tik_stop: function () {
            if (this.timer) {
                clearTimeout(this.timer);
                this.timer = 0;
                this.update_timer = 10000;
            }
        },
        start: function () {
            let res = this._super.apply(this, arguments);
            // // запуск бесконечного цикла отправки, что мы смотрим форму
            if (this.state && this.state.data && this.state.data.id) {
                this.call('bus_service', 'addChannel', this._view_online_form_channel());
                this.call('bus_service', 'onNotification', this, function (notifications) {
                    _.each(notifications, ((notification) => {
                        console.log('notification :>> ', notification, notification[0] == this._view_online_form_channel(), this._view_online_form_channel());
                        if (notification[0] == this._view_online_form_channel()) {
                            this._renderUsersOnline(notification[1]);
                        }
                    }).bind(this));
                })
            }
            return res
        },

        _renderUsersOnline: function (usersOnline = []) {
            // console.log('_renderUsersOnline :>> ', usersOnline);
            this.$el.find('.view_online_button').remove();
            $('.view_online_button').remove();
            let $user_tags = $('<div>');
            $user_tags.addClass("view_online_button");
            usersOnline.forEach((user) => {
                const icon = user.state == "Message.READ" || user.state == "Message.ALIVE_READ" ? 'fa-eye' : 'fa-edit'
                let $button = $('<button>')
                    .addClass("btn btn-primary btn-sm")
                    .css('background-color', user.color)
                    .append(`<span> <img width="25px" height="25px" class="rounded-circle" src="/web/image?model=res.users&amp;field=image_128&amp;id=${user.uid}"  alt="Пользователь"/> ${user.name} <i class="fa fa-1x ${icon}" style="font-size: 1em;"/></span>`)
                // .on('click', _.bind(this._clickShareButton, this));
                $user_tags.append($button);
            })
            this.$el.find('.o_form_sheet').append($user_tags);
        },

    });
});