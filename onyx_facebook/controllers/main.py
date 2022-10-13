# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import json
from urllib import response

import requests
import werkzeug
import ast
import requests
from odoo import http, _
from odoo.http import request
from urllib.parse import urlparse
from urllib.parse import parse_qs
from werkzeug.urls import url_encode, url_join


class SocialFacebookPosts(http.Controller):
    @http.route('/social_facebook_posts', type='http', website=True, auth='public')
    def social_facebook_posts_callbacks(self, **kwargs):
        return 'Hello'


class SocialFacebookPost(http.Controller):
    @http.route('/social_facebook_post/<string:id>', type='http', website=True, auth='public')
    def social_facebook_post_callbacks(self, **kwargs):
        print('im innnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn')
        url = request.httprequest.url
        parsed_url = urlparse(url)
        code = parse_qs(parsed_url.query)['code'][0]
        state = parse_qs(parsed_url.query)['state'][0]

        social_post = request.env['onyx.social.post'].search([], limit=1)
        params = {
            # 'grant_type': 'authorization_code',
            # This is code obtained on previous step by Python script.
            'code': code,
            # This should be same as 'redirect_uri' field value of previous Python script.
            'redirect_uri': social_post._get_facebook_redirect_uri(),
            # Client ID of your created application
            'client_id': request.env['ir.config_parameter'].sudo().get_param('onyx_facebook.client_id_facebook'),
            # # Client Secret of your created application
            'client_secret': request.env['ir.config_parameter'].sudo().get_param(
                'onyx_facebook.client_secret_facebook'),
        }
        res = requests.request('GET', 'https://graph.facebook.com/v6.0/oauth/access_token?%s' % url_encode(params))
        byte_str = res.__dict__['_content']
        dict_str = byte_str.decode("UTF-8")

        my_data = ast.literal_eval(dict_str)
        access_token = my_data.get('access_token')

        from requests.structures import CaseInsensitiveDict

        url = "https://graph.facebook.com/me"

        headers = CaseInsensitiveDict()
        headers["Accept"] = "application/json"
        headers["Authorization"] = "Bearer " + access_token

        resp = requests.get(url, headers=headers)
        byte_str_response = resp.__dict__['_content']
        dict_str_response = byte_str_response.decode("UTF-8")
        my_data_response = ast.literal_eval(dict_str_response)

        profile_id = my_data_response.get('id')
        profile_idd = my_data_response['id']

        urled = "https://graph.facebook.com/" + profile_idd + "/accounts?access_token=" + access_token

        respe = requests.get(urled)

        page_id = respe.json()['data'][0].get('id')
        page_access_token = respe.json()['data'][0].get('access_token')

        fb_social_post = request.env['onyx.social.post'].search([('id', '=', kwargs['id'])])
        message = fb_social_post.message
        post_image = url_join(fb_social_post.get_base_url(), str(fb_social_post.image_ids.image_src))

        post_url = "https://graph.facebook.com/" + str(
            page_id) + '/feed?message=' + message + '&access_token=' + page_access_token
        from requests.structures import CaseInsensitiveDict

        url = "https://graph.facebook.com/" + str(page_id) + "/photos"

        headers = CaseInsensitiveDict()
        headers["Content-x"] = "application/x-www-form-urlencoded"

        data = "url=" + url_join(fb_social_post.get_base_url(), str(fb_social_post.image_ids.website_url))+"&published" \
                                                                                                         "=true&access_token=" + str(page_access_token)
        datas = "url=https://upload.wikimedia.org/wikipedia/commons/2/25/Odoo_12e_homepage.png&published=true" \
               "&access_token=" + str(page_access_token)

        resp = requests.post(url, headers=headers, data=data)

        post = requests.post(post_url)
        media = request.env['onyx.social.media'].search([('onyx_media_type', '=', 'facebook')])
        account = request.env['onyx.social.account'].search([('onyx_media_type', '=', 'facebook')])
        print('my_data_response', my_data_response['name'], media.read())
        if my_data_response['name'] not in account.mapped('name'):
            social_account = request.env['onyx.social.account'].create({
                'name': my_data_response['name'],
                'media_id': media.id,
                'onyx_media_type': 'facebook'
            })
        return request.redirect('/social/home')


class SocialFacebookOnyx(http.Controller):
    @http.route('/social_facebook', type='http', website=True, auth='public')
    def social_facebook_callbacks(self):
        url = request.httprequest.url
        parsed_url = urlparse(url)
        code = parse_qs(parsed_url.query)['code'][0]
        state = parse_qs(parsed_url.query)['state'][0]
        credential = request.env['onyx.social.media'].search([], limit=1)
        params = {
            # 'grant_type': 'authorization_code',
            # This is code obtained on previous step by Python script.
            'code': code,
            # This should be same as 'redirect_uri' field value of previous Python script.
            'redirect_uri': credential._get_facebook_redirect_uri(),
            # Client ID of your created application
            'client_id': request.env['ir.config_parameter'].sudo().get_param('onyx_facebook.client_id_facebook'),
            # # Client Secret of your created application
            'client_secret': request.env['ir.config_parameter'].sudo().get_param(
                'onyx_facebook.client_secret_facebook'),
        }
        res = requests.request('GET', 'https://graph.facebook.com/v6.0/oauth/access_token?%s' % url_encode(params))
        print('rrrrrrrrrrrrrrrrrrr', res, res.__dict__)
        byte_str = res.__dict__['_content']
        dict_str = byte_str.decode("UTF-8")

        my_data = ast.literal_eval(dict_str)
        access_token = my_data.get('access_token')

        print(access_token, 'access_token')
        # response = requests.get(headers=headers)
        from requests.structures import CaseInsensitiveDict

        url = "https://graph.facebook.com/me"

        headers = CaseInsensitiveDict()
        headers["Accept"] = "application/json"
        headers["Authorization"] = "Bearer " + access_token

        resp = requests.get(url, headers=headers)

        byte_str_response = resp.__dict__['_content']
        dict_str_response = byte_str_response.decode("UTF-8")
        my_data_response = ast.literal_eval(dict_str_response)

        media = request.env['onyx.social.media'].search([('onyx_media_type', '=', 'facebook')])
        social_account = request.env['onyx.social.account'].create({
            'name': my_data_response['name'],
            'media_id': media.id,
            'onyx_media_type': 'facebook'
        })
        return request.redirect('/social/home')
