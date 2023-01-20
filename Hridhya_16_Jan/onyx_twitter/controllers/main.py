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
                'client_id': request.uid,
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
    def social_twitter_callbacks_post(self,value):
        # url = request.httprequest.url
        # parsed_url = urlparse(url)
        # oauth_token = request.env['ir.config_parameter'].sudo().get_param('onyx_twitter.oauth_token')
        # oauth_verifier = request.env['ir.config_parameter'].sudo().get_param('onyx_twitter.oauth_verifier')
        # print(parsed_url, 'gehlyicd9tbi7gs', url)
        # print('hfhgshfdjhjg', oauth_verifier, oauth_token)
        # params = {
        #     'oauth_token': oauth_token,
        #     'oauth_verifier': oauth_verifier
        # }
        # res = requests.request('POST', 'https://api.twitter.com/oauth/access_token?%s' % url_encode(params))
        # print(res.text, '00000000000000', res.__dict__)
        # byte_register = res.__dict__['_content']
        # dict_register = byte_register.decode("UTF-8")
        # # my_data_register = ast.literal_eval(dict_register)
        # print(dict_register.split('&'), 'ddddddddddddddd')
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

        print(api, 'dgddddddd')
        print(twitter_image, 'twitter_image')
        print('twitter_image')
        upload_image = twitter_image
        media = api.media_upload(str(twitter_image))

        # Post tweet with image

        tweet = twitter_message

        post_result = api.update_status(status=tweet, media_ids=[media.media_id])
        return request.redirect('/social/home')

