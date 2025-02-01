odoo.define('docx_report.docx_report', function (require) {
"use strict";
  
var core = require('web.core');
var ActionManager = require('web.ActionManager');
var _t = core._t;


ActionManager.include({
    /**
     * Executes actions of type 'ir.actions.report'.
     *
     * @private
     * @param {Object} action the description of the action to execute
     * @param {Object} options @see doAction for details
     * @returns {Deferred} resolved when the action has been executed
     */
    _executeReportAction: function (action, options) {
        var self = this;
        if (action.report_type === 'docx') {
            return self._triggerDownload(action, options, 'docx');
        }
        return this._super.apply(this, arguments);
    },

    /**
     * Generates an object containing the report's urls (as value) for every
     * qweb-type we support (as key). It's convenient because we may want to use
     * another report's type at some point (for example, when `qweb-pdf` is not
     * available).
     *
     * @param {Object} action
     * @returns {Object}
     */
    _makeReportUrls: function (action) {
        var reportUrls = this._super.apply(this, arguments);
        _.extend(reportUrls, {'docx': reportUrls['html'].replace('html','docx')});
        return reportUrls;
    },

});

});
