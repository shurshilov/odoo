odoo.define('tree_list_backlight.tree_list_backlight', function (require) {
"use strict";

    var core = require('web.core');
    var ListView = require('web.ListView');
    var Model = require('web.DataModel');
    var data = require('web.data');
    var _t = core._t;
    var QWeb = core.qweb;

    ListView.List.include({
    get_selection: function () {
        var result = {ids: [], records: []};
        if (!this.options.selectable) {
            return result;
        }
        var records = this.records;
        var self = this;
        self.flagStart = true;
        new Model('ir.config_parameter').call("get_param",["backlight"], {context: new data.CompoundContext()})
                .then(function (result) {
                    if (result.indexOf(self.dataset.model) == -1)
                        self.flagStart = false;
                
                    if (self.flagStart){
                        self.$current.find('td.o_list_record_selector input:not(:checked)').closest('tr').each(function () {  
                            if (this.flag == true){
                                this.style.backgroundColor = "";
                                this.flag = false;
                            }
                        });
                        self.$current.find('td.o_list_record_selector input:checked').closest('tr').each(function () {  
                                this.style.backgroundColor = "rgb(200, 200, 200)";
                                this.flag = true;
                        });
                    }
        });

        this.$current.find('td.o_list_record_selector input:checked')
                .closest('tr').each(function () {
            var record = records.get($(this).data('id'));   
            result.ids.push(record.get('id'));
            result.records.push(record.attributes);
        });

        return result;
    },
    });



});
