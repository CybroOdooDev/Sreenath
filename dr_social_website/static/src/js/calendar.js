odoo.define('social.calendar', function (require) {
"use strict";

var core = require('web.core');
var SocialLinkDialog = require('social.link.dialog');

var _t = core._t;
var QWeb = core.qweb;


const publicWidget = require('web.public.widget');

publicWidget.registry.Calendar = publicWidget.Widget.extend({
    selector: '.o_wsale_products_main_row',
    xmlDependencies: ['/dr_social_website/static/src/xml/calendar.xml'],

    events: {},
    start: function () {
        this._loadCalendar();
        return this._super.apply(this, arguments);

    },
    _loadCalendar: function (ev) {
//        this.$('.tested').append(QWeb.render('SocialCalendar', {widget: ev}));
    },
});


});