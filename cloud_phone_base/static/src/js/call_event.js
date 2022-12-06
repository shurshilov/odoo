//  Copyright 2022 Artem Shurshilov
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


odoo.define('call_event_form', function (require) {
    "use strict";

    const core = require('web.core');
    var BasicRenderer = require('web.BasicRenderer');
    const CallEventDialog = require('call_event_dialog');
    const _t = core._t;

    BasicRenderer.include({
        start: function () {
            let res = this._super.apply(this, arguments);

            if (this.state && this.state.data && this.state.data.id) {
                this.call('bus_service', 'onNotification', this, function (notifications) {
                    _.each(notifications, ((notification) => {
                        if (notification[1].type == "mango_call") {

                            new CallEventDialog(this, {
                                size: 'extra-large',
                                dialogClass: 'o_act_window',
                                model: notification[1].model,
                                id: notification[1].id,
                                title: notification[1].title,
                                subtype: notification[1].subtype,
                                phone: notification[1].phone,
                                call: notification[1].call,
                                name: notification[1].name ? notification[1].name : "",
                                fullscreen: true,
                            }).open();
                        }
                    }).bind(this));
                })
            }
            return res
        },

    });
});