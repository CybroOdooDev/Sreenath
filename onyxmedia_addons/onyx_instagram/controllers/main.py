# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import json
from urllib import response

import requests
import werkzeug
import ast

from odoo import http, _
from odoo.http import request
from urllib.parse import urlparse
from urllib.parse import parse_qs
from werkzeug.urls import url_encode, url_join


class SocialInstagramOnyx(http.Controller):
    @http.route('/social_instagram', type='http', website=True, auth='public')
    def social_instagram_callbacks(self):
        print(self, 'sssssssssssssssssssssssssss', request.httprequest.url)
        media = request.env['onyx.social.media'].search([('onyx_media_type', '=', 'twitter')])
        social_account = request.env['onyx.social.account'].create({
            'name': 'screen_name',
            'media_id': media.id,
            'media_type': 'twitter',
            'dr_account_user_id': request.uid,
            'image': media.image
        })

        # url = request.httprequest.url
        # parsed_url = urlparse(url)
        # code = parse_qs(parsed_url.query)['code'][0]
        # # state = parse_qs(parsed_url.query)['state'][0]
        # credential = request.env['onyx.instagram'].search([], limit=1)
        #
        # access_token = requests.post(
        #     'https://api.instagram.com/oauth/access_token',
        #     params={
        #         'grant_type': 'authorization_code',
        #         # This is code obtained on previous step by Python script.
        #         'code': code,
        #         # This should be same as 'redirect_uri' field value of previous Python script.
        #         'redirect_uri': credential._get_linkedin_redirect_uri(),
        #         # Client ID of your created application
        #         'client_id': credential.client_id_instagram,
        #         # Client Secret of your created application
        #         'client_secret': credential.client_secret_instagram,
        #     },
        # ).json()['access_token']
        # print('access_token',access_token)
        # # headers = {
        # #     'Content-type': 'application/json',
        # #     'X-Restli-Protocol-Version': '2.0.0',
        # #     'Authorization': 'Bearer ' +access_token
        # # }
        # # res = requests.request('GET', 'https://api.linkedin.com/v2/me',headers=headers)
        # # print('rrrrrrrrrrrrrrrrrrr',res, res.__dict__['_content'])
        # # byte_str = res.__dict__['_content']
        # # dict_str = byte_str.decode("UTF-8")
        # # my_data = ast.literal_eval(dict_str)
        # # #
        # # print(id,'ffffffffffffffffffffffffffffffffffffffffff', my_data)
        # # profile_id = my_data.get('id')
        # #
        # # # scope: w_member_social,r_liteprofile
        # # access_token = 'YOUR_ACCESS_TOKEN'
        # #
        # # url = "https://api.linkedin.com/v2/ugcPosts"
        # #
        # #
        # #
        # # post_data = {
        # #     "author": "urn:li:person:" + profile_id,
        # #     "lifecycleState": "PUBLISHED",
        # #     "specificContent": {
        # #         "com.linkedin.ugc.ShareContent": {
        # #             "shareCommentary": {
        # #                 "text": "Hello World! This is my first Share onxxxxxxxxxxxxxxxxxxxxxxxx LinkedIn!mmmmmmmmmmm!"
        # #             },
        # #             "shareMediaCategory": "NONE"
        # #         }
        # #     },
        # #     "visibility": {
        # #         "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        # #     }
        # # }
        # #
        # # response = requests.post(url, headers=headers, json=post_data)
        # #
        # # print(response)
        # """
        # We can receive
        # - code directly from LinkedIn
        # - access_token from IAP
        # - state from LinkedIn/IAP, the state avoid the CSRF attack
        # """
        # # if not request.env.user.has_group('social.group_social_manager'):
        # #     return request.render('social.social_http_error_view',
        # #                           {'error_message': _('Unauthorized. Please contact your administrator.')})
        # #
        # # if kw.get('error') not in ('user_cancelled_authorize', 'user_cancelled_login'):
        # #     if not access_token and not code:
        # #         return request.render('social.social_http_error_view',
        # #                               {'error_message': _('LinkedIn did not provide a valid access token.')})
        # #
        # #     media = request.env.ref('social_linkedin.social_media_linkedin')
        # #
        # #     if media.csrf_token != state:
        # #         return request.render('social.social_http_error_view',
        # #                               {'error_message': _('There was a authentication issue during your request.')})
        #
        # # try:
        # # if not access_token:
        # #     access_token = self._linkedin_get_access_token(code)
        #
        # # request.env['social.account']._create_linkedin_accounts(access_token, media)
        #
        # # Both _get_linkedin_access_token and _create_linkedin_accounts may raise a SocialValidationException
        # # except SocialValidationException as e:
        # #     return request.render('social.social_http_error_view', {'error_message': str(e)})

        return 'Helloooooo'

    # ========================================================
    # COMMENTS / LIKES
    # ========================================================

    # @http.route('/social_linkedin/comment', type='http', auth='user', methods=['POST'])
    # def social_linkedin_add_comment(self, stream_post_id, message=None, comment_id=None, **kwargs):
    #     print('jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj')
    #     stream_post = self._get_social_stream_post(stream_post_id, 'linkedin')
    #     return json.dumps(stream_post._linkedin_comment_add(message, comment_id))
    #
    # @http.route('/social_linkedin/delete_comment', type='json', auth='user')
    # def social_linkedin_delete_comment(self, stream_post_id, comment_id, **kwargs):
    #     stream_post = self._get_social_stream_post(stream_post_id, 'linkedin')
    #     return stream_post._linkedin_comment_delete(comment_id)
    #
    # @http.route('/social_linkedin/get_comments', type='json', auth='user')
    # def social_linkedin_get_comments(self, stream_post_id, comment_urn=None, offset=0, comments_count=20):
    #     stream_post = self._get_social_stream_post(stream_post_id, 'linkedin')
    #     return stream_post._linkedin_comment_fetch(
    #         comment_urn=comment_urn,
    #         offset=offset,
    #         count=comments_count
    #     )
    #
    # # ========================================================
    # # MISC / UTILITY
    # # ========================================================
    #
    # def _linkedin_get_access_token(self, linkedin_authorization_code):
    #     """
    #     Take the `authorization code` and exchange it for an `access token`
    #     We also need the `redirect uri`
    #
    #     :return: the access token
    #     """
    #     linkedin_url = 'https://www.linkedin.com/oauth/v2/accessToken'
    #     linkedin_app_id = request.env['ir.config_parameter'].sudo().get_param('social.linkedin_app_id')
    #     linkedin_client_secret = request.env['ir.config_parameter'].sudo().get_param('social.linkedin_client_secret')
    #     media = request.env['onyx.linkedin']
    #     params = {
    #         'grant_type': 'authorization_code',
    #         'code': linkedin_authorization_code,
    #         'redirect_uri': media._get_linkedin_redirect_uri(),
    #         'client_id': linkedin_app_id,
    #         'client_secret': linkedin_client_secret
    #     }
    #
    #     response = requests.post(linkedin_url, data=params, timeout=5).json()
    #
    #     error_description = response.get('error_description')
    #     if error_description:
    #         raise SocialValidationException(error_description)
    #
    #     return response.get('access_token')
