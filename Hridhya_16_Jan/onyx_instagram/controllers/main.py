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

import logging
import pprint

_logger = logging.getLogger(__name__)


class SocialInstagramOnyx(http.Controller):
    @http.route('/social_instagram', type='http', website=True, auth='public')
    def social_instagram_callbacks(self):
        print(self, 'sssssssssssssssssssssssssss', request.httprequest.url)
        _logger.info("***********************************************************")

        _logger.info("sssssssssssssssssssssssssss:%s", pprint.pformat(request.httprequest.url))

        url = request.httprequest.url
        parsed_url = urlparse(url)
        code = parse_qs(parsed_url.query)['code'][0]
        # state = parse_qs(parsed_url.query)['state'][0]
        credential = request.env['onyx.instagram'].search([], limit=1)
        _logger.info("jjjjjjjjjjjjjjjj:%s", pprint.pformat(code))
        #         access_token = requests.post(
        #             'https://api.instagram.com/oauth/access_token',
        #             params={
        #                 'client_id': credential.client_id_instagram,
        #                 'client_secret': credential.client_secret_instagram,
        #                 'grant_type': 'authorization_code',
        #                 'redirect_uri': credential._get_instagram_redirect_uri(),
        #                 'code': code,

        #                 # This is code obtained on previous step by Python script.
        #                 # This should be same as 'redirect_uri' field value of previous Python script.
        #                 # Client ID of your created application
        #                 # Client Secret of your created application
        #             },
        #         )
        params = {
                     'grant_type': 'authorization_code',
                     # This is code obtained on previous step by Python script.
                     'code': code,
                     # This should be same as 'redirect_uri' field value of previous Python script.
                     'redirect_uri': credential._get_instagram_redirect_uri(),
                     # Client ID of your created application
                     'client_id': credential.client_id_instagram,
                     # Client Secret of your created application
                     'client_secret': credential.client_secret_instagram,
                 },

        request_body = {
            "client_id": f"{credential.client_id_instagram}",
            "client_secret": f"{credential.client_secret_instagram}",
            "grant_type": "authorization_code",
            "code": f"{code}",
            "redirect_uri": f"{credential._get_instagram_redirect_uri()}",
        }

        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        _logger.info("!!!!!!!!!!!!!!!!!!!!!!!!!!!:%s", pprint.pformat(headers))
        response = requests.post('https://api.instagram.com/oauth/access_token', data=request_body, headers=headers)
        #         res = requests.request('POST', 'https://api.instagram.com/oauth/access_token?client_id=900387824684082&client_secret=50a5aad7229364ab5550f00517110793&grant_type=authorization_code&redirect_uri=https://cybroodoodev-demo-repo.odoo.com/social_instagram&code=code')
        #         _logger.info("ressssssssssssssssssssssssssssss:%s", pprint.pformat(response['access_token']))
        _logger.info(" response.json:%s", pprint.pformat(response.json()))
        return request.redirect('/social/home')