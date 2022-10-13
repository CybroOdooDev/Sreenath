# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import json
from urllib import response

import requests
import tweepy
import werkzeug
import ast

from odoo import http, _
from odoo.http import request
from urllib.parse import urlparse
from urllib.parse import parse_qs
from werkzeug.urls import url_encode, url_join


class SocialTwitterOnyx(http.Controller):
    @http.route('/social_twitter/callback', type='http', website=True, auth='public')
    def social_twitter_callbacks(self, **kwargs):
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!', kwargs)

        url = request.httprequest.url
        parsed_url = urlparse(url)
        oauth_token = parse_qs(parsed_url.query)['oauth_token'][0]
        oauth_verifier = parse_qs(parsed_url.query)['oauth_verifier'][0]
        print(parsed_url, 'gehlyicd9tbi7gs', url)
        print('hfhgshfdjhjg', oauth_verifier, oauth_token)
        params = {
            'oauth_token': oauth_token,
            'oauth_verifier': oauth_verifier
        }

        res = requests.request('POST', 'https://api.twitter.com/oauth/access_token?%s' % url_encode(params))
        print(res.text, '00000000000000', res.__dict__)
        byte_register = res.__dict__['_content']
        dict_register = byte_register.decode("UTF-8")
        # my_data_register = ast.literal_eval(dict_register)
        print(dict_register.split('&'), 'ddddddddddddddd')
        oauth_token = dict_register.split('&')[0].split('=')[1]
        oauth_token_secret = dict_register.split('&')[1].split('=')[1]
        user_id = dict_register.split('&')[2].split('=')[1]
        screen_name = dict_register.split('&')[3].split('=')[1]
        print(oauth_token_secret, 'kkkkkkkkkkkkkk')
        request.env['ir.config_parameter'].sudo().set_param('onyx_twitter.oauth_token', oauth_token)
        request.env['ir.config_parameter'].sudo().set_param('onyx_twitter.oauth_verifier', oauth_token_secret)

        twitter_consumer_key = request.env['ir.config_parameter'].sudo().get_param('onyx_twitter.consumer_key')
        twitter_consumer_secret_key = request.env['ir.config_parameter'].sudo().get_param(
            'onyx_twitter.consumer_secret_key')
        twitter_oauth_token = request.env['ir.config_parameter'].sudo().get_param('onyx_twitter.oauth_token')
        twitter_oauth_verifier = request.env['ir.config_parameter'].sudo().get_param('onyx_twitter.oauth_verifier')
        print('oauth_token..............', twitter_oauth_token)
        print('oauth_verifier..............', twitter_oauth_verifier)

        # model = request.env['onyx.twitter'].search([],limit=1)
        # auth = tweepy.OAuthHandler(twitter_consumer_key, twitter_consumer_secret_key)
        # auth.set_access_token(oauth_token, oauth_token_secret)
        # # auth.set_access_token(model.access_token, model.access_token_secret)
        #
        # api = tweepy.API(auth)

        media = request.env['onyx.social.media'].search([('onyx_media_type', '=', 'twitter')])
        account = request.env['onyx.social.account'].search([('onyx_media_type', '=', 'twitter')])

        if screen_name not in account.mapped('name'):
            social_account = request.env['onyx.social.account'].create({
                'name': screen_name,
                'media_id': media.id,
                'onyx_media_type': 'twitter',
                'dr_account_user_id': request.uid,
                'image': media.image
            })
        # # Upload image
        # status = "Flower flowerss"
        # api.update_status(status=status)
        # # media = api.media_upload("/home/cybrosys/Pictures/Screenshot from 2022-08-22 15-57-29.png")
        # print(api, 'dgddddddd')
        # media = api.media_upload("/home/cybrosys/Pictures/2560px-Odoo_logo.svg.png")
        #
        # # Post tweet with image
        #
        # tweet = "Flowers"
        # post_result = api.update_status(status=tweet, media_ids=[media.media_id])

        return request.redirect('/social_twitter_post/callback')

        # post_result = api.update_status(status=tweet, media_ids=[media.media_id])


class SocialTwitterPostOnyx(http.Controller):
    @http.route('/social_twitter_post/callback', type='http', website=True, auth='public')
    def social_twitter_callbacks(self):
        url = request.httprequest.url
        parsed_url = urlparse(url)
        oauth_token = request.env['ir.config_parameter'].sudo().get_param('onyx_twitter.oauth_token')
        oauth_verifier = request.env['ir.config_parameter'].sudo().get_param('onyx_twitter.oauth_verifier')
        print(parsed_url, 'gehlyicd9tbi7gs', url)
        print('hfhgshfdjhjg', oauth_verifier, oauth_token)
        params = {
            'oauth_token': oauth_token,
            'oauth_verifier': oauth_verifier
        }
        res = requests.request('POST', 'https://api.twitter.com/oauth/access_token?%s' % url_encode(params))
        print(res.text, '00000000000000', res.__dict__)
        byte_register = res.__dict__['_content']
        dict_register = byte_register.decode("UTF-8")
        # my_data_register = ast.literal_eval(dict_register)
        print(dict_register.split('&'), 'ddddddddddddddd')
        oauth_token = request.env['ir.config_parameter'].sudo().get_param('onyx_twitter.oauth_token')
        oauth_token_secret = request.env['ir.config_parameter'].sudo().get_param('onyx_twitter.oauth_verifier')
        # user_id = dict_register.split('&')[2].split('=')[1]
        # screen_name = dict_register.split('&')[3].split('=')[1]
        print(oauth_token_secret, 'kkkkkkkkkkkkkk')

        twitter_consumer_key = request.env['ir.config_parameter'].sudo().get_param('onyx_twitter.consumer_key')
        twitter_consumer_secret_key = request.env['ir.config_parameter'].sudo().get_param(
            'onyx_twitter.consumer_secret_key')

        # model = request.env['onyx.twitter'].search([],limit=1)
        auth = tweepy.OAuthHandler(twitter_consumer_key, twitter_consumer_secret_key)
        auth.set_access_token(oauth_token, oauth_token_secret)
        # auth.set_access_token(model.access_token, model.access_token_secret)

        api = tweepy.API(auth)
        # media = request.env['onyx.social.media'].search([('onyx_media_type', '=', 'twitter')])
        # social_account = request.env['onyx.social.account'].create({
        #     'name': screen_name,
        #     'media_id': media.id,
        #     'onyx_media_type': 'twitter',
        #     'dr_account_user_id': request.uid,
        #     'image': media.image
        # })
        # # Upload image
        twitter_message = request.env['ir.config_parameter'].sudo().get_param('onyx_twitter.twitter_message')
        twitter_image = request.env['ir.config_parameter'].sudo().get_param('onyx_twitter.twitter_image')

        status = 'twitter_messages'
        api.update_status(status=status)
        media = api.media_upload("/home/cybrosys/Documents/onyx media/odoo-apps-pic1.png")
        print(api, 'dgddddddd')
        print(twitter_image, 'twitter_image')
        upload_image = twitter_image
        # media = api.media_upload("https://www.confianzit.com/assets/images/odoo-apps/odoo-apps-pic1.jpg")

        # Post tweet with image

        tweet = twitter_message

        post_result = api.update_status(status=tweet, media_ids=[media.media_id])
        return request.redirect('/social/home')

    #     url = request.httprequest.url
    #     parsed_url = urlparse(url)
    #     code = parse_qs(parsed_url.query)['code'][0]
    #     state = parse_qs(parsed_url.query)['state'][0]
    #     credential = request.env['onyx.linkedin'].search([],limit=1)
    #
    #     print(code,state)
    #     import requests
    #     access_token = requests.post(
    #         'https://www.linkedin.com/oauth/v2/accessToken',
    #         params={
    #             'grant_type': 'authorization_code',
    #             # This is code obtained on previous step by Python script.
    #             'code': code,
    #             # This should be same as 'redirect_uri' field value of previous Python script.
    #             'redirect_uri': credential._get_linkedin_redirect_uri(),
    #             # Client ID of your created application
    #             'client_id': credential.client_id,
    #             # # Client Secret of your created application
    #             'client_secret': credential.client_secret,
    #         },
    #     ).json()['access_token']
    #     print('access_token',access_token)
    #     headers = {
    #         'Content-type': 'application/json',
    #         'X-Restli-Protocol-Version': '2.0.0',
    #         'Authorization': 'Bearer ' +access_token
    #     }
    #     res = requests.request('GET', 'https://api.linkedin.com/v2/me',headers=headers)
    #     print('rrrrrrrrrrrrrrrrrrr',res, res.__dict__['_content'])
    #     byte_str = res.__dict__['_content']
    #     dict_str = byte_str.decode("UTF-8")
    #     my_data = ast.literal_eval(dict_str)
    #     #
    #     print(id,'ffffffffffffffffffffffffffffffffffffffffff', my_data)
    #     profile_id = my_data.get('id')
    #
    #     # scope: w_member_social,r_liteprofile
    #     access_token = 'YOUR_ACCESS_TOKEN'
    #
    #     url = "https://api.linkedin.com/v2/ugcPosts"
    #
    #
    #
    #     post_data = {
    #         "author": "urn:li:person:" + profile_id,
    #         "lifecycleState": "PUBLISHED",
    #         "specificContent": {
    #             "com.linkedin.ugc.ShareContent": {
    #                 "shareCommentary": {
    #                     "text": "Hello World! This is my first Share onxxxxxxxxxxxxxxxxxxxxxxxx LinkedIn!mmmmmmmmmmm!"
    #                 },
    #                 "shareMediaCategory": "NONE"
    #             }
    #         },
    #         "visibility": {
    #             "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
    #         }
    #     }
    #
    #     response = requests.post(url, headers=headers, json=post_data)
    #
    #     print(response)
    #     """
    #     We can receive
    #     - code directly from LinkedIn
    #     - access_token from IAP
    #     - state from LinkedIn/IAP, the state avoid the CSRF attack
    #     """
    #     # if not request.env.user.has_group('social.group_social_manager'):
    #     #     return request.render('social.social_http_error_view',
    #     #                           {'error_message': _('Unauthorized. Please contact your administrator.')})
    #     #
    #     # if kw.get('error') not in ('user_cancelled_authorize', 'user_cancelled_login'):
    #     #     if not access_token and not code:
    #     #         return request.render('social.social_http_error_view',
    #     #                               {'error_message': _('LinkedIn did not provide a valid access token.')})
    #     #
    #     #     media = request.env.ref('social_linkedin.social_media_linkedin')
    #     #
    #     #     if media.csrf_token != state:
    #     #         return request.render('social.social_http_error_view',
    #     #                               {'error_message': _('There was a authentication issue during your request.')})
    #
    #     # try:
    #     # if not access_token:
    #     #     access_token = self._linkedin_get_access_token(code)
    #
    #     # request.env['social.account']._create_linkedin_accounts(access_token, media)
    #
    #     # Both _get_linkedin_access_token and _create_linkedin_accounts may raise a SocialValidationException
    #     # except SocialValidationException as e:
    #     #     return request.render('social.social_http_error_view', {'error_message': str(e)})
    #
    #
    # # ========================================================
    # # COMMENTS / LIKES
    # # ========================================================
    #
    # # @http.route('/social_linkedin/comment', type='http', auth='user', methods=['POST'])
    # # def social_linkedin_add_comment(self, stream_post_id, message=None, comment_id=None, **kwargs):
    # #     print('jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj')
    # #     stream_post = self._get_social_stream_post(stream_post_id, 'linkedin')
    # #     return json.dumps(stream_post._linkedin_comment_add(message, comment_id))
    # #
    # # @http.route('/social_linkedin/delete_comment', type='json', auth='user')
    # # def social_linkedin_delete_comment(self, stream_post_id, comment_id, **kwargs):
    # #     stream_post = self._get_social_stream_post(stream_post_id, 'linkedin')
    # #     return stream_post._linkedin_comment_delete(comment_id)
    # #
    # # @http.route('/social_linkedin/get_comments', type='json', auth='user')
    # # def social_linkedin_get_comments(self, stream_post_id, comment_urn=None, offset=0, comments_count=20):
    # #     stream_post = self._get_social_stream_post(stream_post_id, 'linkedin')
    # #     return stream_post._linkedin_comment_fetch(
    # #         comment_urn=comment_urn,
    # #         offset=offset,
    # #         count=comments_count
    # #     )
    # #
    # # # ========================================================
    # # # MISC / UTILITY
    # # # ========================================================
    # #
    # # def _linkedin_get_access_token(self, linkedin_authorization_code):
    # #     """
    # #     Take the `authorization code` and exchange it for an `access token`
    # #     We also need the `redirect uri`
    # #
    # #     :return: the access token
    # #     """
    # #     linkedin_url = 'https://www.linkedin.com/oauth/v2/accessToken'
    # #     linkedin_app_id = request.env['ir.config_parameter'].sudo().get_param('social.linkedin_app_id')
    # #     linkedin_client_secret = request.env['ir.config_parameter'].sudo().get_param('social.linkedin_client_secret')
    # #     media = request.env['onyx.linkedin']
    # #     params = {
    # #         'grant_type': 'authorization_code',
    # #         'code': linkedin_authorization_code,
    # #         'redirect_uri': media._get_linkedin_redirect_uri(),
    # #         'client_id': linkedin_app_id,
    # #         'client_secret': linkedin_client_secret
    # #     }
    # #
    # #     response = requests.post(linkedin_url, data=params, timeout=5).json()
    # #
    # #     error_description = response.get('error_description')
    # #     if error_description:
    # #         raise SocialValidationException(error_description)
    # #
    # #     return response.get('access_token')
