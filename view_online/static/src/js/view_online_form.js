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

odoo.define('view_online_form', function(require) {
    "use strict";

    var core = require('web.core');
    var FormRenderer = require('web.FormRenderer');
    var _t = core._t;

    FormRenderer.include({
        end_count: 100,
        start_count: 0,
        update_timer: 20,
        colors: ["#3CC157", "#2AA7FF", "#1B1B1B", "#FCBC0F", "#F85F36"],
        // отправляем всем пользователям какую форму мы смотрим
        _sendStatusOnlineViewForm: async function(){
            this.start_count+= 1;
            if (this.__parentedParent && this.__parentedParent.initialState && this.__parentedParent.initialState.res_id)
            this._rpc({
                route: '/longpolling/send/viewonline',
                params: {
                    channel: 'view.online.form',
                    message: {
                        model: this.__parentedParent.initialState.model,
                        res_id: this.__parentedParent.initialState.res_id,
                        uid: this.__parentedParent.initialState.context.uid,
                        mode: this.mode
                    },
                }
            },{ shadow: true })
        },

        // запрос каждые update_timer секунд
        _loopUpdateStatusOnlineViewForm: function() {
            setTimeout(async () => {
                await this._sendStatusOnlineViewForm();
                // удаляем если давно не получали ответа от пользователя
                if (this.usersOnline)
                for (let i=0; i < this.usersOnline.length; i++){
                    const now = new Date().getTime()/1000;
                    if ((now - this.usersOnline[i]['time']) > 1.2*this.update_timer) {
                        this.usersOnline = await this.usersOnline.filter( el => el.uid != this.usersOnline[i].uid ); 
                        this._renderUserOnline();
                    }
                }
                if (this.start_count > this.end_count)
                    return
                this._loopUpdateStatusOnlineViewForm();
            }, this.update_timer * 1000);
        },

        start: function(){
            let res = this._super.apply(this, arguments);

            this.usersOnline = [];
            // запуск бесконечного цикла отправки, что мы смотрим форму
            this._loopUpdateStatusOnlineViewForm();

            // получение любого мессенджа
            this.call('bus_service', 'onNotification', this, function (notifications) {
                _.each(notifications, ( (notification) => {
                    if (notification[0][1] === 'view.online.form') {                        
                        // если получили сообщение что кто-то смотрит ту форму которую мы, то отображаем его
                        if (notification[1].model == this.__parentedParent.initialState.model ||
                            notification[1].res_id == this.__parentedParent.initialState.res_id) {

                            // добавляем время последнего обновления
                            notification[1]['time'] = new Date().getTime()/1000;
                            // Добавляем пользователя онлайн, если его еще не было
                            // создаем нового или обновляем
                            const index = this.usersOnline.findIndex(item => item.uid === notification[1].uid)
                            if (index == -1){
                                notification[1]['color'] = this.colors[Math.floor(Math.random() * this.colors.length)]
                                this.usersOnline.push(notification[1])
                            }
                            else {
                                // сохраняем цвет уже добавленном
                                notification[1]['color'] = this.usersOnline[index]['color'];
                                this.usersOnline[index] = notification[1];
                            }

                            this._renderUserOnline();
                        }
                    }
                }).bind(this));
            });
            setTimeout(async () => {
                await this._sendStatusOnlineViewForm();
            }, 2 * 1000);
            return res;
        },

		_renderUserOnline: function() {
            this.$el.find('.view_online_button').remove();
            $('.view_online_button').remove();
            let $user_tags = $('<div>');
            $user_tags.addClass("view_online_button");
            for (let i in this.usersOnline){
                // скрываем текущего юзера
                if (Number(this.usersOnline[i].uid) == Number(this.__parentedParent.initialState.context.uid))
                    continue;
                let $button = $('<button>').addClass("btn btn-primary btn-sm");
                $button.css('background-color', this.usersOnline[i].color)
                if (this.usersOnline[i].mode == "readonly")
                    $button.append('<span>'+ this.usersOnline[i].user_name + 
                        ' <i class="fa fa-1x fa-eye" style="font-size: 1em;"/></span>');
                else
                    $button.append('<span>'+ this.usersOnline[i].user_name + 
                        ' <i class="fa fa-1x fa-edit" style="font-size: 1em;"/></span>');

                $user_tags.append($button);
                //$button.on('click', _.bind(this._clickShareButton, this));
            }
            this.$el.find('.o_form_sheet').append($user_tags);
        },

	});
});