# -*- coding: utf-8 -*-
# Copyright (c) 2019-Present Droggol Infotech Private Limited. (<https://www.droggol.com/>)

from odoo import http, _
from odoo.http import request


class SocialMain(http.Controller):

    @http.route(['/social/home'], type='http', auth='user', sitemap=False, website=True)
    def social_home(self, **kw):
        linked_accounts = request.env['onyx.social.account'].search([('dr_account_user_id', '=', request.env.uid)])
        print('linked_accounts',linked_accounts)
        onboarding_finished = request.env['res.users'].search([('id', '=', request.env.uid)])
        print(onboarding_finished,onboarding_finished.onboarding)
        if not linked_accounts:
            request.session['isOnbording'] = True
        return request.render('dr_social_website.home', {
            'linked_accounts': linked_accounts,
            'onboarding_finished': onboarding_finished,
            # 'isOnbording': request.session['isOnbording']
        })

    @http.route(['/social/get_media'], type='json', auth='user_sudo')
    def social_get_media(self, **kw):
        return request.env['onyx.social.media'].search_read([('onyx_has_streams', '=', True), ('onyx_media_type', 'not in', ['youtube', 'push_notifications'])], ['name', 'onyx_media_type'])

    @http.route(['/social/add_media_account/<int:media_id>'], type='json', auth='user_sudo')
    def social_add_media_account(self, media_id, **kw):
        media = request.env['onyx.social.media'].browse(media_id)
        print('kkkkkksssssssssssssssjjjjjjjjjjj')
        return media._action_add_account_onyx()

    @http.route(['/social/thank_you'], type='http', auth='user', sitemap=False, website=True)
    def social_thank_you(self):
        request.session['isOnbording'] = False
        return request.render('dr_social_website.dr_thankyou')
