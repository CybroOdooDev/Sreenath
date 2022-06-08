odoo.define('social.portal', function (require) {
"use strict";

var core = require('web.core');
var SocialLinkDialog = require('social.link.dialog');

var _t = core._t;
var qweb = core.qweb;

const publicWidget = require('web.public.widget');

publicWidget.registry.SocialLinkBtn = publicWidget.Widget.extend({
    selector: '.dr_website_social',
    events: {
        'click .dr_social_link' : '_onClick',
        'click .dr_relink_btn' : '_onClickMedia',
    },
    start: function () {
        this.isOnboarding = this.$target.hasClass('dr-onboarding-mode');
        if (this.isOnboarding) {
            this._openDialog();
        }
    },
    _openDialog: function () {
        var dialog = new SocialLinkDialog(this, {
            title: _t('Link Social Accountsss'),
            size: 'medium',
            renderFooter: false
        });
        dialog.open();
    },

    _onClick: function () {
        this._openDialog();
    },
    _onClickMedia: function (ev) {
        var $target = $(ev.currentTarget);
        var mediaId = $target.data('mediaId');
        this._rpc({
            route: `/social/add_media_account/${mediaId}`,
            params: {}
        }).then((result) => {
            if (result.url) {
                window.location.href = result.url;
            }
        });
    }

});


});