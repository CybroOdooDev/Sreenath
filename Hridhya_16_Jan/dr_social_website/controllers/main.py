# -*- coding: utf-8 -*-
# Copyright (c) 2019-Present Droggol Infotech Private Limited. (<https://www.droggol.com/>)

from odoo import http, _
from odoo.http import request
import requests
from odoo.exceptions import UserError


class SocialMain(http.Controller):

    @http.route(['/social/home'], type='http', auth='user', sitemap=False, website=True)
    def social_home(self, **kw):
        linked_accounts = request.env['onyx.social.account'].search([('dr_account_user_id', '=', request.env.uid)])
        print('linked_accounts',linked_accounts)
        onboarding_finished_user = request.env['res.users'].search([('id', '=', request.env.uid)])
        if not linked_accounts:
            request.session['isOnbording'] = True
        ayrshare_api_key = request.env['ir.config_parameter'].sudo().get_param('dr_social_website.ayrshare_api_key')
        if ayrshare_api_key:
            payload = {'title': str(onboarding_finished_user.name)}
            headers = {'Content-Type': 'application/json',
                       'Authorization': 'Bearer ' + ayrshare_api_key}

            profile = requests.post('https://app.ayrshare.com/api/profiles/profile',
                              json=payload,
                              headers=headers)

            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!', profile.json())
            profile_data = profile.json()

            if profile_data['status'] == 'success':

                profile_key = profile_data['profileKey']
                onboarding_finished_user.sudo().write({"profile_key": profile_key})
                onboarding_finished_user.sudo().partner_id.write({"profile_key": profile_key})

        else:
            raise UserError(_(
                'Please contact administrator to update the Ayrshare API Key in Settings'
            ))

        return request.render('dr_social_website.home', {
            'linked_accounts': linked_accounts,
            'onboarding_finished': onboarding_finished_user,
            # 'isOnbording': request.session['isOnbording']
        })

    @http.route(['/social/get_media'], type='json', auth='user_sudo')
    def social_get_media(self, **kw):
        return request.env['onyx.social.media'].search_read([('onyx_has_streams', '=', True), ('onyx_media_type', 'not in', ['youtube', 'push_notifications'])], ['name', 'onyx_media_type'])

    @http.route(['/social/add_media_account/<int:media_id>'], type='json', auth='user')
    def social_add_media_account(self, media_id, **kw):

        ayrshare_api_key = request.env['ir.config_parameter'].sudo().get_param('dr_social_website.ayrshare_api_key')

        with open('/home/cybrosys/PycharmProjects/odoo15E/odoo15/onyxmedia_latest/Hridhya_16_Jan/dr_social_website/onyxm.key') as f:
            profileKey = f.read()
        print('***********', request.env.user.read())
        print('***********', request.env.user.name)
        print('!!!!!!!!!!', request.env.user.profile_key)
        payload = {'domain': 'testing',
                   'privateKey': profileKey,
                   'profileKey': '000WXDV-PYF4QYQ-J5WQD4B-MR9QJ2D'}
        print('payload', payload)
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer ' + ayrshare_api_key}

        media_urls = requests.post('https://app.ayrshare.com/api/profiles/generateJWT',
                                   json=payload,
                                   headers=headers)

        print(media_urls.json())
        return {
            'type': 'ir.actions.act_url',
            'url': 'https://www.facebook.com/v6.0/dialog/oauth?%s' % url_encode(params),
            'target': 'self'
        }

    @http.route(['/social/thank_you'], type='http', auth='user', sitemap=False, website=True)
    def social_thank_you(self):
        request.session['isOnbording'] = False
        return request.render('dr_social_website.dr_thankyou')
