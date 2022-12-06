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

odoo.define('call_event_dialog', function(require) {
    "use strict";

    var core = require('web.core');
    var _t = core._t;
    var Dialog = require('web.Dialog');


    var CallEventDialog = Dialog.extend({
        template: 'CallEventDialog',

        init: function(parent, options) {
            this.options = options;
            self = this;

            this._super(parent, _.extend({
                buttons: [
                    {
                        text: _t("Перейти к записи"),
                        classes: 'btn-primary',
                        close: true,
                        click: () => {
                            const action = {
                                type: 'ir.actions.act_window',
                                name: "Call lead",
                                res_model: self.options.model,
                                res_id: self.options.id,
                                view_mode: 'form',
                                views: [[false, 'form']],
                            };
                            self.do_action(action);
                        }
                    },
                    {
                        text: _t("Закрыть"),
                        classes: 'btn-warning',
                        close: true
                    },

                ]
            }, options || {}));
        },

        start: function() {
            return this._super.apply(this, arguments).then(() => {
                setTimeout(() => {
                    this.close()
                  }, 15000)
            });
        },

    });

    return CallEventDialog
});