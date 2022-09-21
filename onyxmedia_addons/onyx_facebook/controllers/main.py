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


class SocialFacebookOnyx(http.Controller):
    @http.route('/social_facebook', type='http', website=True, auth='public')
    def social_facebook_callbacks(self):
        print(self, 'iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii', request.httprequest.url)
        url = request.httprequest.url
        parsed_url = urlparse(url)
        code = parse_qs(parsed_url.query)['code'][0]
        state = parse_qs(parsed_url.query)['state'][0]
        credential = request.env['onyx.facebook'].search([], limit=1)
        #
        print(code, state)

        # access_token = requests.post(
        #     'https://www.linkedin.com/oauth/v2/accessToken',
        params = {
            # 'grant_type': 'authorization_code',
            # This is code obtained on previous step by Python script.
            'code': code,
            # This should be same as 'redirect_uri' field value of previous Python script.
            'redirect_uri': credential._get_facebook_redirect_uri(),
            # Client ID of your created application
            'client_id': credential.client_id_facebook,
            # # Client Secret of your created application
            'client_secret': credential.client_secret_facebook,
        }
        # ).json()['access_token']
        # print('access_token',a                                                                                                                                                         ccess_token)

        res = requests.request('GET', 'https://graph.facebook.com/v6.0/oauth/access_token?%s' % url_encode(params))
        print('rrrrrrrrrrrrrrrrrrr', res, res.__dict__)
        byte_str = res.__dict__['_content']
        dict_str = byte_str.decode("UTF-8")

        my_data = ast.literal_eval(dict_str)
        #
        # print(id,'ffffffffffffffffffffffffffffffffffffffffff', my_data,5092885444154093)
        access_token = my_data.get('access_token')
        # headers = {
        #     'Accept ': 'application/json',
        #     # 'X-Restli-Protocol-Version': '2.0.0',
        #     'Authorization': 'Bearer ' + access_token
        # }
        print(access_token, 'access_token')
        # response = requests.get(headers=headers)
        from requests.structures import CaseInsensitiveDict

        url = "https://graph.facebook.com/me"

        headers = CaseInsensitiveDict()
        headers["Accept"] = "application/json"
        headers["Authorization"] = "Bearer " + access_token

        resp = requests.get(url, headers=headers)

        print(resp, 'kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk')

        # print('responseeeeeeee',response)
        byte_str_response = resp.__dict__['_content']
        print(byte_str_response, 'byte_str_response')
        dict_str_response = byte_str_response.decode("UTF-8")
        my_data_response = ast.literal_eval(dict_str_response)
        #
        profile_id = my_data_response.get('id')
        print('nnnnnnnnnnnnnnnnnnnnnnn', my_data_response, profile_id, resp.__dict__)
        print('my_data_response', my_data_response)
        profile_idd = my_data_response['id']
        #
        #

        urled = "https://graph.facebook.com/" + profile_idd + "/accounts?access_token=" + access_token
        print('ddddddddddd', urled)

        respe = requests.get(urled)


        var = {'data': [{
            'access_token': 'EAAQJZAqCtWKUBAPek0kRvTKqW6BgHZAeMu7YLqpDThaa2bdc65H1MH1EfpXyDMzcq5no07obRqXa8cbZALOekdIIc'
                            'ByZB1JkUFsHBo6zz59tiZCLJ6xrJnfKojSG'
                            't9ch0OUtn2CTsI6YudLZBvNc8xglYbVfj1JZBoSVWBl9YHvNQY7KbfhL5gx',
            'category': 'Product/service',
            'category_list': [{'id': '2201', 'name': 'Product/service'}],
            'name': 'hrid_diya',
            'id': '101035916062196',
            'tasks': ['ANALYZE', 'ADVERTISE', 'MESSAGING', 'MODERATE', 'CREATE_CONTENT', 'MANAGE']}, {
            'access_token': 'EAAQJZAqCtWKUBAJmYzompAfRYRT2f70KXRHyc9JRJ0TccsiW91jqb7AnCZBK41fyDtH2svdTtZAb7xdKlGHmAXgC'
                            'UQwDb7e5tiPiXwJhepoUercfBo0mGt9'
                            'vynXykQDfXCBiyEVykChfhK7dQNoiXk6fvOCvmlUEhPrYSBYhzJWX9Og44Np',
            'category': 'Dancer',
            'category_list': [{'id': '1614', 'name': 'Dancer'}],
            'name': 'Dance',
            'id': '110914318389618',
            'tasks': ['ANALYZE', 'ADVERTISE', 'MESSAGING', 'MODERATE', 'CREATE_CONTENT', 'MANAGE']}, {
            'access_token': 'EAAQJZAqCtWKUBAOxHFsaj95gkz24cFsCkix9yG9ZAyIQvdv0kHbTYajv0h4sNghZCDiNfRHctUk5ELYeylZBZ'
                            'CqZA8hiloDPZAsZA8IpMhuGnFSZCeLO8CzdJcr'
                            ' jJ37546Ql6QvZATaFq3Ez7wXnT62eZBkQ5QM0JOBHxowmj5JZCoc7uy69ghYEQLvo',
            'category': 'Movie/television studio',
            'category_list': [{'id': '370369022981015', 'name': 'Movie/television studio'},
                              {'id': '1105', 'name': 'Movie'}], 'name': 'TwisTmedias',
            'id': '242511199234385',
            'tasks': ['ANALYZE', 'ADVERTISE', 'MESSAGING', 'MODERATE', 'CREATE_CONTENT', 'MANAGE']}],
            'paging': {'cursors': {'before': 'MTAxMDM1OTE2MDYyMTk2', 'after': 'MjQyNTExMTk5MjM0Mzg1'}}}

        print(respe.status_code)
        print(respe.json())

        page_id = respe.json()['data'][0].get('id')
        page_access_token = respe.json()['data'][0].get('access_token')
        print('page_id', page_id)
        print('page_access_token', page_access_token)
        message = 'hiiiiiiiiiiiiiiqqqqqqqqqqqiiii'
# B581318997
#         026201004689
        # social_post
        # 4838340262018534
        # C1-00000027536480-C1
        # 80 - C1
        post_url = "https://graph.facebook.com/"+str(page_id)+'/feed?message='+message+'&access_token='+page_access_token
        from requests.structures import CaseInsensitiveDict

        url = "https://graph.facebook.com/"+str(page_id)+"/photos"

        headers = CaseInsensitiveDict()
        headers["Content-x"] = "application/x-www-form-urlencoded"

        data = "url=https://upload.wikimedia.org/wikipedia/commons/2/25/Odoo_12e_homepage.png&published=true" \
               "&access_token="+str(page_access_token)

        resp = requests.post(url, headers=headers, data=data)

        # print(resp.status_code)
        # print('post_url', post_url)
        # post = requests.post(post_url)
        # print('post', post.json())
        #
        # media_result = requests.post(
        #     url_join(
        #         'https://graph.facebook.com/v14.0',
        #         "/%s/media" % page_id
        #     ),
        #     data={
        #         'caption': message,
        #         'access_token': page_access_token,
        #         'image_url': 'data:image/jpeg;base64,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'
        #     },
        #     timeout=10
        # )
        # urlss = "https://graph.facebook.com/101035916062196/photos?access_token=EAAQJZAqCtWKUBAOz1QE6TFBWON19assxUALuZCvIiFNZCQtyf5IvtpARSycjxzUjUsvxZAQTXZAx2hgEQThx8s0ZBApOh47LU4V7AZAsHDHLkLFu1b4dZChZChYQ9lE1mTAVt5dZCLP72OPnpy4Fe2k6RDUgzamNt7ehoLOoSoRRnDQyk23Dq3mj4Y"
        #
        # respss = requests.get(urlss)
        #
        # print(respss.status_code)
        #
        # print('media_result', media_result.json())


        # post_url = "https://graph.facebook.com/101035916062196/feed?message=Smarteveryfamily&access_token=
        # EAAQJZAqCtWKUBAPek0kRvTKqW6BgHZAeMu7YLqpDThaa2bdc65H1MH1EfpXyDMzcq5no07obRqXa8cbZALOekdIIcByZB1JkUFsHB
        # o6zz59tiZCLJ6xrJnfKojSGt9ch0OUtn2CTsI6YudLZBvNc8xglYbVfj1JZBoSVWBl9YHvNQY7KbfhL5gx"

        # # # scope: w_member_social,r_liteprofile
        # # access_token = 'YOUR_ACCESS_TOKEN'
        # #
        # # url = "https://api.linkedin.com/v2/ugcPosts"

        # #

        # for rec in sel
        # #
        # #
        # # post_data = {
        # #     "author": "urn:li:person:" + profile_id,
        # #     "lifecycleState": "PUBLISHED",
        # #     "specificContent": {
        # #         "com.linkedin.ugc.ShareContent": {
        # #             "shareCommentary": {
        # #                 "text": "Hello World! This is my first Share onxxxxxxxxxxxxxxxxxxxxx LinkedIn!mmmmmmmmmmm!"
        # #             },
        # #             "shareMediaCategory": "NONE"
        # #         }
        # #     },
        # #     "visibility": {
        # #         "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        # #     }
        # # }
        # # #
        # # response = requests.post(url, headers=headers, json=post_data)
        # #
        # # print(response.text,'hhhhhhhhhhhhhhhhhhhhhhhhhhhhh')
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
        #
        # return 'Helloooooo'

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
