odoo.define('res_partner_skype.widget', function (require) {
'use strict';

var field_registry = require('web.field_registry');
var basic_fields = require('web.basic_fields');

var FieldSkype = basic_fields.FieldEmail.extend({
    prefix: 'skype',
});

   field_registry.add('skype', FieldSkype);
   return {
        FieldSkype: FieldSkype
    };
});
