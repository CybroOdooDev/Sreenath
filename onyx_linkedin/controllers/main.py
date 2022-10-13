# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import base64
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


class SocialLinkedinOnyxPost(http.Controller):
    @http.route('/social_linkedin_post', type='http', website=True, auth='public')
    def social_linkedin_post(self, httpReq=None):
        url = request.httprequest.url
        parsed_url = urlparse(url)
        code = parse_qs(parsed_url.query)['code'][0]
        state = parse_qs(parsed_url.query)['state'][0]
        credential = request.env['onyx.social.media'].search([('onyx_media_type', '=', 'linkedin')])
        social_post = request.env['onyx.social.post'].search([], limit=1)
        print(code, state)
        # access_token = requests.post(
        #     'https://www.linkedin.com/oauth/v2/accessToken',
        #     params={
        #         'grant_type': 'authorization_code',
        #         # This is code obtained on previous step by Python script.
        #         'code': code,
        #         # This should be same as 'redirect_uri' field value of previous Python script.
        #         'redirect_uri': social_post._get_linkedin_post_redirect_uri(),
        #         # Client ID of your created application
        #         'client_id': request.env['ir.config_parameter'].sudo().get_param('onyx_linkedin.client_id'),
        #         # # Client Secret of your created application
        #         'client_secret': request.env['ir.config_parameter'].sudo().get_param('onyx_linkedin.client_secret'),
        #     },
        # ).json()['access_token']
        access_token = request.env['ir.config_parameter'].sudo().get_param('onyx_linkedin.linkedin_access_token')
        print('access_token', access_token)
        headers = {
            'Content-type': 'application/json',
            'X-Restli-Protocol-Version': '2.0.0',
            'Authorization': 'Bearer ' + access_token
        }
        print(headers)
        res = requests.request('GET', 'https://api.linkedin.com/v2/me', headers=headers)
        print('rrrrrrrrrrrrrrrrrrr', res, res.__dict__['_content'])
        byte_str = res.__dict__['_content']
        dict_str = byte_str.decode("UTF-8")
        my_data = ast.literal_eval(dict_str)
        #
        print(id, 'ffffffffffffffffffffffffffffffffffffffffff', my_data, my_data.get('localizedFirstName'))
        profile_id = my_data.get('id')
        user_name = my_data.get('localizedFirstName') + ' ' + my_data.get('localizedLastName')

        # scope: w_member_social,r_liteprofile
        # access_token = 'YOUR_ACCESS_TOKEN'
        print('profile_id', profile_id, user_name)

        url_register = 'https://api.linkedin.com/v2/assets?action=registerUpload'
        register = {

            "registerUploadRequest": {
                "recipes": [
                    "urn:li:digitalmediaRecipe:feedshare-image"
                ],
                "owner": "urn:li:person:" + profile_id,
                "serviceRelationships": [
                    {
                        "relationshipType": "OWNER",
                        "identifier": "urn:li:userGeneratedContent"
                    }
                ]

            }
        }
        register_response = requests.post(url_register, headers=headers, json=register)

        print(register_response.__dict__['_content'])
        byte_register = register_response.__dict__['_content']
        dict_register = byte_register.decode("UTF-8")
        my_data_register = ast.literal_eval(dict_register)
        print(my_data_register, 'll')
        upload_url_register = my_data_register.get('value')["uploadMechanism"]
        upload_url = upload_url_register.get('com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest')['uploadUrl']
        print(upload_url, 'kkkkkk')
        asset = my_data_register.get('value')['asset']
        print('asset', asset)

        linkedin_message = request.env['ir.config_parameter'].sudo().get_param('onyx_linkedin.linkedin_message')
        linkedin_image = request.env['ir.config_parameter'].sudo().get_param('onyx_linkedin.linkedin_image')
        url = "https://api.linkedin.com/v2/shares"

        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }

        payload = {
            "content": {
                "contentEntities": [
                    {
                        "entityLocation": "https://www.google.com",
                        "thumbnails": [
                            {
                                "resolvedUrl": "https://images.pexels.com/photos/2115217/pexels-photo-2115217.jpeg"
                            },
                        ]
                    }
                ],
                "title": linkedin_message
            },
            'distribution': {
                'linkedInDistributionTarget': {}
            },
            'owner': "urn:li:person:" + profile_id,
            'text': {
                'text': linkedin_message
            }
        }

        response = requests.post(url=url, headers=headers, json=payload)

        print(response.json())
        print('ggggggggggggg', request.uid)
        media = request.env['onyx.social.media'].search([('onyx_media_type', '=', 'linkedin')])
        account = request.env['onyx.social.account'].search([('onyx_media_type', '=', 'linkedin')])
        print('my_data_response', user_name, )

        if user_name not in account.mapped('name'):
            print('mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm',
                  account.mapped('name'))
            social_account = request.env['onyx.social.account'].create({
                'name': user_name,
                'media_id': media.id,
                'onyx_media_type': 'linkedin',
                'dr_account_user_id': request.uid,
                'image': media.image
            })

        return request.redirect('/social/home')


class SocialLinkedinOnyx(http.Controller):
    @http.route('/social_linkedinss', type='http', website=True, auth='public')
    def social_linkedin_callbacks(self, httpReq=None):
        print(self, 'sssssssssssssssssssssssssss', request.httprequest.url)

        url = request.httprequest.url
        parsed_url = urlparse(url)
        code = parse_qs(parsed_url.query)['code'][0]
        state = parse_qs(parsed_url.query)['state'][0]
        credential = request.env['onyx.social.media'].search([('onyx_media_type', '=', 'linkedin')])

        # url = "https://www.linkedin.com/oauth/v2/accessToken"
        #
        # payload = 'grant_type=authorization_code&code=%s&client_id=%s&client_secret=%s&redirect_uri=%s' %(code, request.env['ir.config_parameter'].sudo().get_param('onyx_linkedin.client_id'), request.env['ir.config_parameter'].sudo().get_param('onyx_linkedin.client_secret'), credential._get_linkedin_redirect_uri())
        # headers = {
        #     'Content-Type': 'application/x-www-form-urlencoded',
        # }
        #
        # response = requests.request("POST", url, headers=headers, data=payload)
        #
        # print(response.text)

        params = {
                     'grant_type': 'authorization_code',
                     # This is code obtained on previous step by Python script.
                     'code': code,
                     # This should be same as 'redirect_uri' field value of previous Python script.
                     'redirect_uri': credential._get_linkedin_redirect_uri(),
                     # Client ID of your created application
                     'client_id': request.env['ir.config_parameter'].sudo().get_param('onyx_linkedin.client_id'),
                     # # Client Secret of your created application
                     'client_secret': request.env['ir.config_parameter'].sudo().get_param(
                         'onyx_linkedin.client_secret'),
                 },

        # access_token = requests.post('https://www.linkedin.com/oauth/v2/accessToken?%s') % url_encode(params)
        #
        print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaayyyyyyyyyyyyyyyyyyyy',params)
        access_token = requests.post(
            'https://www.linkedin.com/oauth/v2/accessToken',
            params={
                'grant_type': 'authorization_code',
                # This is code obtained on previous step by Python script.
                'code': code,
                # This should be same as 'redirect_uri' field value of previous Python script.
                'redirect_uri': credential._get_linkedin_redirect_uri(),
                # Client ID of your created application
                'client_id': request.env['ir.config_parameter'].sudo().get_param('onyx_linkedin.client_id'),
                # # Client Secret of your created application
                'client_secret': request.env['ir.config_parameter'].sudo().get_param('onyx_linkedin.client_secret'),
            },
        ).json()['access_token']
        print('access_token', access_token)

        linkedin_access_token = request.env['ir.config_parameter'].sudo().set_param('onyx_linkedin.linkedin_access_token', access_token)

        headers = {
            'Content-type': 'application/json',
            'X-Restli-Protocol-Version': '2.0.0',
            'Authorization': 'Bearer ' + access_token
        }
        print(headers)
        res = requests.request('GET', 'https://api.linkedin.com/v2/me', headers=headers)
        print('rrrrrrrrrrrrrrrrrrr', res, res.__dict__['_content'])
        byte_str = res.__dict__['_content']
        dict_str = byte_str.decode("UTF-8")
        my_data = ast.literal_eval(dict_str)
        #
        print(id, 'ffffffffffffffffffffffffffffffffffffffffff', my_data, my_data.get('localizedFirstName'))
        profile_id = my_data.get('id')
        user_name = my_data.get('localizedFirstName') + ' ' + my_data.get('localizedLastName')

        # scope: w_member_social,r_liteprofile
        # access_token = 'YOUR_ACCESS_TOKEN'
        print('profile_id', profile_id, user_name)

        url_register = 'https://api.linkedin.com/v2/assets?action=registerUpload'
        register = {

            "registerUploadRequest": {
                "recipes": [
                    "urn:li:digitalmediaRecipe:feedshare-image"
                ],
                "owner": "urn:li:person:" + profile_id,
                "serviceRelationships": [
                    {
                        "relationshipType": "OWNER",
                        "identifier": "urn:li:userGeneratedContent"
                    }
                ]

            }
        }
        register_response = requests.post(url_register, headers=headers, json=register)

        print(register_response.__dict__['_content'])
        byte_register = register_response.__dict__['_content']
        dict_register = byte_register.decode("UTF-8")
        my_data_register = ast.literal_eval(dict_register)
        print(my_data_register, 'll')
        upload_url_register = my_data_register.get('value')["uploadMechanism"]
        upload_url = upload_url_register.get('com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest')['uploadUrl']
        print(upload_url, 'kkkkkk')
        asset = my_data_register.get('value')['asset']
        print('asset', asset)
        # # parsed_url_upload = urlparse(upload_url)
        # with open('/home/cybrosys/Downloads/pexels-pixabay-60597.jpg', 'rb') as f:
        #     data = f.read()
        #
        # print(requests, 'dddddddddddd')
        #
        # url_new = upload_url
        # image = open("/home/cybrosys/Downloads/pexels-pixabay-60597.jpg", "rb").read()
        # images = base64.b64encode(image)
        # print('imagessssssssssssssssss', images)
        # headers = {
        #     "Authorization": f"Bearer %s" % access_token
        # }
        # social_post = request.env['onyx.social.post'].search([], limit=1)
        # print(social_post.read())
        linkedin_message = request.env['ir.config_parameter'].sudo().get_param('onyx_linkedin.linkedin_message')
        linkedin_image = request.env['ir.config_parameter'].sudo().get_param('onyx_linkedin.linkedin_image')
        url = "https://api.linkedin.com/v2/shares"

        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }

        payload = {
            "content": {
                "contentEntities": [
                    {
                        "entityLocation": "https://www.google.com",
                        "thumbnails": [
                            {
                                "resolvedUrl": "https://images.pexels.com/photos/2115217/pexels-photo-2115217.jpeg"
                            },
                        ]
                    }
                ],
                "title": linkedin_message
            },
            'distribution': {
                'linkedInDistributionTarget': {}
            },
            'owner': "urn:li:person:" + profile_id,
            'text': {
                'text': linkedin_message
            }
        }

        media = request.env['onyx.social.media'].search([('onyx_media_type', '=', 'linkedin')])
        account = request.env['onyx.social.account'].search([('onyx_media_type', '=', 'linkedin')])
        print('my_data_response', user_name,)

        if user_name not in account.mapped('name'):
            print('mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm', account.mapped('name'))
            social_account = request.env['onyx.social.account'].create({
                'name': user_name,
                'media_id': media.id,
                'onyx_media_type': 'linkedin',
                'dr_account_user_id': request.uid,
                'image': media.image
            })

        return request.redirect('/social/home')

