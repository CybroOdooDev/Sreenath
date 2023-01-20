odoo.define('dr_social_website.link.dialog', function (require) {
"use strict";
console.log('kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk')
var core = require('web.core');
var Dialog = require('web.Dialog');

var _t = core._t;
var qweb = core.qweb;

$(document).ready(function (ev) {
console.log('ssssssssssssssssssssssssssssssssss')

//    $('.o_footer').addClass('header_hide')F
//    $('.navbar').addClass('d-none')
    $('nav a[href^="/' + location.pathname.split("/")[1] + '"]').addClass('active');
})

var SocialLinkDialog = Dialog.extend({
    template: 'social.link.dialog',
    xmlDependencies: (Dialog.prototype.xmlDependencies || []).concat(['/dr_social_website/static/src/xml/dialog.xml']),
    events: {
        "click .dr_media_card": '_onClickMedia',
    },
    /**
     * @override
     * @param {Object} options
     */
    init: function (parent, options) {
        options = options || {};
        this._super(parent, $.extend(true, {}, options));
    },

    /**
     * @override
     */
    willStart: function () {
        var getMediaTypes = this._rpc({
            route: '/social/get_media',
            params: {}
        }).then((result) => {
            this.media = result;
            console.log(this.media);
        });
        return Promise.all([
            this._super.apply(this, arguments),
            getMediaTypes
        ]);
    },

    _onClickMedia: function (ev) {
    console.log('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        var $target = $(ev.currentTarget);
        var mediaId = $target.data('mediaId');
        this._rpc({
            route: `/social/add_media_account/${mediaId}`,
            params: {}
        }).then((result) => {
            if (result.url) {
                window.location.href = result.url;
                console.log('ppppppppppppppppppppp')
            }
        });
    }
});

return SocialLinkDialog;
});