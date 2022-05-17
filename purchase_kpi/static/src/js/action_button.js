odoo.define('purchase_kpi.action_button', function (require) {
"use strict";
var core = require('web.core');
var ListController = require('web.ListController');
var rpc = require('web.rpc');
var session = require('web.session');
var _t = core._t;

ListController.include({
   renderButtons: function($node) {
   this._super.apply(this, arguments);
       if (this.$buttons) {
         this.$buttons.find('.oe_action_button').click(this.proxy('receive_invoice')) ;
       }
   },

   action_def: function () {
            var self =this
            var user = session.uid;
            rpc.query({
                model: 'product.template',
                method: 'get_values',
                args: [[user],{'id':user}],
                });
            },

            receive_invoice: function () {
            var self = this
            var user = session.uid;
            rpc.query({
                model: 'product.template',
                method: 'get_values',
                args: [[user],{'id':user}],
                }).then(function (viewID) {
                self.do_action({
                    name: _t('Last Year Purchase KPI'),
                    type: 'ir.actions.act_window',
                    res_model: 'product.template',
                    views: [[viewID, 'list']],
                    view_mode: 'list',
                    target: 'new',
                });
                });
            },

});
});