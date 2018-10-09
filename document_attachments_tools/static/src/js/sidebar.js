/**********************************************************************************
*    Copyright (C) 2018 Eyekraft, Artem Shurshilov
**********************************************************************************/

odoo.define('document_attachments_tools.SidebarPreview', function (require) {
"use strict";

var Sidebar = require('web.Sidebar');
var Model = require("web.Model");
var session = require('web.session');
var data = require('web.data');
var Attachment = new Model('ir.attachment', session.user_context);

Sidebar.include({
    start: function() {
    	this._super.apply(this, arguments);
    	this.$el.on('click','.o_sidebar_edit_attachment', this.on_attachment_edit);
    },

	on_attachment_save: function(){
		var self = this;
		var value = this.$el.find('.oe_input_field_name').val();
		Attachment.call("write",[this.rec_id,{'name':value}], {context: new data.CompoundContext()});
		_.each(this.items.files, function(file) {if (file.id == self.rec_id) file.label = value;});
		this.redraw();
	},

	on_attachment_cancel: function(){
		this.redraw();
	},
    
    on_attachment_rename: function(e) {
    	e.preventDefault();
        e.stopPropagation();
    },

    on_attachment_edit: function(e) {
        e.preventDefault();
        e.stopPropagation();
        this.rec_id = $(e.currentTarget).data('id');
        this.parentElement = $(e.currentTarget)[0].parentElement;
        var oldText = this.parentElement.innerText;
        var parentNode = this.parentElement.parentElement;
        parentNode.innerHTML="<input class='oe_input_field_name' value='" + oldText +
        	"''><button class='btn btn-primary btn-sm o_form_button_edit oe_input_button_name'>Save</button>" +
			"<button class='btn btn-primary btn-sm o_form_button_edit oe_input_button_cancel'>Cancel</button>";
        this.$el.find('.oe_input_field_name').click(this.on_attachment_rename);
        this.$el.find('.oe_input_button_name').click(this.on_attachment_save);
        this.$el.find('.oe_input_button_cancel').click(this.on_attachment_cancel);
    },
});

});