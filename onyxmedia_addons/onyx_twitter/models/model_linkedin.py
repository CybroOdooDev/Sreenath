# import secrets
#
# import requests
# import webbrowser
import requests
from odoo import fields, models
# import logging
from werkzeug.urls import url_encode, url_join
#
# _logger = logging.getLogger(__name__)
# try:
#     # import mechanize
#     from linkedin_v2 import linkedin
#     # from urllib.request import HTTPRedirectHandler as MechanizeRedirectHandler
# except:
#     print('g')
#
import numpy as np
import tweepy
import requests
import base64

#
class OnyxTwitter(models.Model):
    _name = "onyx.twitter"


    consumer_key = fields.Char(string="Api Key")
    consumer_secret_key = fields.Char(string="Api Secret")
    # ac ss_token_secret = fields.Char(string="Access Secret")

#     client_id = fields.Char(string="Client Id")
#     client_secret = fields.Char(string="Client Secret")
#
#     # redirect_uri = fields.Char(string="Redirect uri")
#
    def button_twitter(self):
        print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        # importing all dependencies

        # variables for accessing twitter API
        # consumer_key = 'JetQ00yNQPghXlBtdgbGryqdt'
        # consumer_secret_key = 'o5jhB9GiA0dinhIpB33g0dNNv6lr2adRjvUWZelgWQQQlDuyWo'
        # access_token = '1559781504582303744-H0jAn2i83BYPYYnjjUfVSFREaCUkYm'
        # access_token_secret = '11cLsWkz3mb4Pd7O532Ce7Bpahty2vpZwLi8MbRURXAB7'
        callback_url = url_join(self.get_base_url(), "social_twitter/callback")

        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret_key, callback_url)
        # auth.set_access_token(self.access_token, self.access_token_secret)
        api = tweepy.API(auth)
        print(api,'apiiiiii')
        # Reformat the keys and encode them
        key_secret = '{}:{}'.format(self.consumer_key, self.consumer_secret_key).encode('ascii')
        # Transform from bytes to bytes that can be printed
        b64_encoded_key = base64.b64encode(key_secret)
        # Transform from bytes back into Unicode
        b64_encoded_key = b64_encoded_key.decode('ascii')
        print('b64_encoded_key',b64_encoded_key)
        base_url = 'https://api.twitter.com/'
        auth_url = '{}oauth2/token'.format(base_url)
        auth_headers = {
            'Authorization': 'Basic {}'.format(b64_encoded_key),
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
        }
        auth_data = {
            'grant_type': 'client_credentials'
        }
        print(base_url,'llll',auth_url,'jjjj',auth_headers)
        auth_resp = requests.post(auth_url, headers=auth_headers, data=auth_data)
        print(auth_resp.status_code, auth_resp)
        access_token = auth_resp.json()['access_token']
        print(access_token,'accesstoken')
        #
        api = tweepy.API(auth)
        try:
            redirect_url = auth.get_authorization_url()
            print(redirect_url,'redirect')
            return {
                'type': 'ir.actions.act_url',
                'url': redirect_url,
                'target': 'self'
            }
        except tweepy.TweepError:
            print(
            'Error! Failed to get request token.')
        #
        # # Upload image
        # status = "This is my first mn,,nnnnnn xnnnnzxnnnlnnnpost to Twitter using the ewAPI. I am still learning, please be kind :)"
        # api.update_status(status=status)
        # # media = api.media_upload("/home/cybrosys/Pictures/Screenshot from 2022-08-22 15-57-29.png")
        # print(api,'dgddddddd')
        # media = api.media_upload("/home/cybrosys/Pictures/Screenshot from 2022-08-22 15-57-29.png")
        #
        # # Post tweet with image
        #
        # tweet = "Great things take time"
        #
        # post_result = api.update_status(status=tweet, media_ids=[media.media_id])

        # token = session.get('request_token')

        # file = open('/home/cybrosys/Pictures/Screenshot from 2022-08-22 15-57-29.png', 'rb')
        # data = file.read()
        # resource_url = 'https://upload.twitter.com/1.1/media/upload.json'
        # print(resource_url)
        # upload_image = {
        #     'media': data,
        #     'media_category': 'tweet_image'}
        #
        # image_headers = {
        #     'Authorization': 'Bearer {}'.format(access_token)
        # }
        #
        # media_id = requests.post(resource_url, headers=image_headers, params=upload_image)
        # print(media_id)

        # api_key = 'LaoGlSiil4pN0MIeZQ5k3OfmV'
        # api_secrets = '39Pc6pjGOLAG81acmGahCx8MPzTXEYJw3mQPB0lNrkUJj3PH7z'
        # access_token = '1559781504582303744-IpM4Q5QjJ36XBQZLlVTrV6EhpoVUBo'
        # access_secret = 'GiNHivuBW6sAekLz0XhAGPRjGIzrlNwu9BTcy9iWhP1T3'
        #
        # # Authenticate to Twitter
        # auth = tweepy.OAuthHandler(api_key, api_secrets)
        # auth.set_access_token(access_token, access_secret)
        # print(auth,'kkkkk')
        # api = tweepy.API(auth)
        # print('api',api.__dict__)
        #
        # try:
        #     api.verify_credentials()
        #     print('Successful Authentication')
        # except:
        #     print('Failed authentication')
#         # urls = "https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=78us1mshswd8km" \
#         #        "&redirect_uri=https://www.linkedin.com/developers/tools/oauth/redirect" \
#         #        "&state=foo&scope=w_member_social,r_liteprofile,w_organization_social"
#         # # print('gggggggggggggggggg')
# #         # authentication_url = 'https://api.linkedin.com/v2/me'
#         credentials = {
# #         #     'response_type': 'code',
# #         #     'client_id': self.client_id,
# #         #     'client_secret': self.client_secret,
# #         #     'redirect_uri': 'https://www.linkedin.com/developers/tools/oauth/redirect',
# #         #     'code': 'foo',
# #         #     'grant_type': 'authorization_code',
# #
#             'consumer_key': 'LaoGlSiil4pN0MIeZQ5k3OfmV',
#             'consumer_secret': '39Pc6pjGOLAG81acmGahCx8MPzTXEYJw3mQPB0lNrkUJj3PH7z',
#         }
#         # print(authentication_url, 'dsffffff', credentials)
# #         # headers = {
# #         #     'Content-type': 'application/json',
# #         #     'Authorization': 'Bearer' + 'AQVCCNFp-ffS1h5xSnm_CVR3yMxJfMUgQDMqKZhX_t4npFuy_8AJyJsirNfF4aZ2pauTQoIbYJpz4gZxtoMYxPZ_ZIs4buhkHFfrBjk_WKeHKIiCibXp-CqdkQUpWfHQE7rqVzH5s_Lrabs_Qo938UYux_mozcEFd9NP-FtgwPTMc-Xjc0PLo-v5fofAIgJvo6ACBxitSdoLGA-4Ugcp4i3sDmSt1e2A8ccuDY_PulJSRsKzVHlgWLDJNUmXrmr31G4CynYoHqIWBSEvur7F1hWiMdGOfMD2DEXlZOh-yfX3j4cZVGIpb8KPPbUgUrp18Ku8cZV4qP0s2TAhKGZjc6Qr1ujHWA'
# #         # }
#         headers = {
#             'Content-type': 'application/json',
#         }
# #         # session = requests.Session()
# #         # # r = session.post(authentication_url,
# #         # #                  data=credentials, headers=headers)
#         request_token = 'https://api.twitter.com/oauth/request_token'
#         headers = {'oauth_callback': url_join(self.get_base_url(), "social_twitter/callback")}
#
#         r = requests.request('GET', request_token,
#                              data=credentials, headers=headers)
#         print('jfdkhslkgjhshc hvqyixdau',r)
# #         # res = requests.request('GET', urls)
# #         #
#         #
#         # print('res', urls)
#         # print(res, 'rrrrrrrrrrrr')
#         # print('ressssssssss',res.text)
#         # # li_credential = {}
#         # return webbrowser.open(urls)
#         # redirect_uri = 'https://www.linkedin.com/developers/tools/oauth/redirect'
#
#         # url = requests.Request(
#         #     'GET',
#         #     'https://www.linkedin.com/oauth/v2/authorization',
#         #     params={
#         #         'response_type': 'code',  # Always should equal to fixed string "code"
#         #
#         #         # ClientID of your created application
#         #         'client_id': self.client_id,
#         #         'redirect_uri': 'https://www.linkedin.com/developers/tools/oauth/redirect',
#         #         'state': secrets.token_hex(8).upper(),
#         #         'scope': 'r_liteprofile,r_emailaddress,w_member_social',
#         #     },
#         # ).prepare().url
#         # auth_url = "https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=78us1mshswd8km" \
#         #        "&redirect_uri=https://www.linkedin.com/developers/tools/oauth/redirect" \
#         #        "&state=foo&scope=w_member_social,r_liteprofile,w_organization_social"
#
        # auth = requests.request('GET', auth_url,  params={
        #         'response_type': 'code',  # Always should equal to fixed string "code"
#         #
#         #         # ClientID of your created application
#         #         'client_id': self.client_id,
#         #         'redirect_uri': 'https://www.linkedin.com/developers/tools/oauth/redirect',
#         #         'state': secrets.token_hex(8).upper(),
#         #         'scope': 'r_liteprofile,r_emailaddress,w_member_social',
#         #     }, headers=header)
#         #
#         # print(auth_url,'llllllllllllllllllllllllll')
#         # # print('LLLLLLLLLLLLLLLLLLL', auth_url.text)
#
#         params = {
# #             'response_type': 'code',
# #             'client_id': self.client_id,
# #             'redirect_uri': self._get_linkedin_redirect_uri(),
# #             'state': '123456',
# #             'scope': 'r_liteprofile r_emailaddress w_member_social rw_organization_admin w_organization_social r_organization_social'
#             'oath_token': '1559781504582303744-IpM4Q5QjJ36XBQZLlVTrV6EhpoVUBo'
#         }
# #
#         return {
#             'type': 'ir.actions.act_url',
#             'url': 'https://api.twitter.com/oauth/authorize?%s' % url_encode(params),
#             'target': 'self'
#         }
#
#     def _get_linkedin_redirect_uri(self):
#         return url_join(self.get_base_url(), '/social_linkedinss')
#
#
#         # import mechanize
#         # from linkedin import linkedin
#         # import mechanicalsoup
#         # from urllib.parse import parse_qs
#         # from urllib.parse import urlsplit
#         #
#         # from urllib.request import HTTPRedirectHandler as MechanizeRedirectHandler
#         #
#         # li_credential = {}
#         # br = mechanicalsoup.StatefulBrowser()
#         # br.set_cookiejar(mechanize.CookieJar())
#         # li_permissions = ['r_liteprofile', 'r_emailaddress', 'w_share', 'rw_company_admin', 'w_member_social']
#         #
#         # auth = linkedin.LinkedInAuthentication(self.client_id,
#         #                                        self.client_secret,
#         #                                        redirect_uri,
#         #                                        li_permissions)
#         # print('auth............', auth)
#         # print('br............', br)
#         # print('///////////////////', br.get_url())
#         #
#         # try:
#         #     br.open(auth)
#         #     br.select_form(selector='form', nr=0)
#         #     br['session_key'] = li_credential['un']
#         #     br['session_password'] = li_credential['pw']
#         #     br.submit_selected()
#         #     try:
#         #         authorization_code = parse_qs(urlsplit(br.get_url()).query)['code']
#         #         print('vode', authorization_code)
#         #     except:
#         #         br.open(br.get_url())
#         #         br.select_form(selector='form', nr=1)
#         #         q = br.submit_selected()
#         #         auth.authorization_code = parse_qs(urlsplit(br.get_url()).query)['code']
#         #         if not auth.authorization_code:
#         #             raise Warning("Please check Redirect URLs in the LinkedIn app settings!!!!!!!!!!!!")
#         # except:
#         #     print('ppppppppppppp')
#         #
#         # li_suit_credent = {}
#         # li_suit_credent['access_token'] = str(auth.get_access_token().access_token)
#         # member_url = 'https://api.linkedin.com/v2/me'
#         # response = self.get_urn('GET', member_url, li_suit_credent['access_token'])
#         # urn_response_text = response.json()
#         #
#         # li_credential['profile_urn'] = urn_response_text['id']
#         #
#         # li_suit_credent['li_credential'] = li_credential
#         # print('sssssssssssss', urn_response_text)
#         # print('li_suit_credent', li_suit_credent)
#
#         # return {
#         #     'type': 'ir.actions.act_url',
#         #     'url': 'https://www.linkedin.com/oauth/v2/authorization?%s' % url_encode(params),
#         #     'target': 'self'
#         # }
# # ----------------------------------------------------------------------------------------------------------------------
#         # # linkedin_auth_provider = self.env.ref('hr_linkedin_recruitment.provider_linkedin')
#         # # if linkedin_auth_provider.client_id and linkedin_auth_provider.client_secret:
#         # li_credential['api_key'] = self.client_id
#         # li_credential['secret_key'] = self.client_secret
#         # print(li_credential['api_key'], li_credential['secret_key'], '[[[[[[[[[[[[[')
#         # else:
#         #     raise ValidationError(_('LinkedIn Access Credentials are empty.!\n'
#         #                             'Please fill up in Auth Provider form.'))
#
#         # if self.env['ir.config_parameter'].sudo().get_param('recruitment.li_username'):
#         #     li_credential['un'] = self.env['ir.config_parameter'].sudo().get_param('recruitment.li_username')
#         #     print(li_credential['un'], 'uuuuuuuuuuuuuuuuuuuuu')
#         # else:
#         #     raise exceptions.Warning(_('Please fill up username in LinkedIn Credential settings.'))
#
#         # if self.env['ir.config_parameter'].sudo().get_param('recruitment.li_password'):
#         #     li_credential['pw'] = self.env['ir.config_parameter'].sudo().get_param('recruitment.li_password')
#         #     print(li_credential['pw'])
#         # else:
#         #     raise exceptions.Warning(_('Please fill up password in LinkedIn Credential settings.'))
#
#         # Browser Data Posting And Signing
#         # br = mechanicalsoup.StatefulBrowser()
#         # br.set_cookiejar(mechanize.CookieJar())
#         # return_uri = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
#         # print(return_uri, 'iiiiiiiiiiiii')
#         # li_permissions = ['r_liteprofile', 'r_emailaddress', 'w_member_social']
#         # print(li_permissions)
#         # auth = linkedin.LinkedInAuthentication(li_credential['api_key'],
#         #                                        li_credential['secret_key'],
#         #                                        return_uri,
#         #                                        li_permissions)
#         # print(auth, 'brrrrr')
#
#         # session = requests.Session()
#         # r = session.post(authentication_url,
#         #                  data=credentials, headers=headers)
#         # r = requests.request('GET',authentication_url,
#         #                  data=(li_credential['api_key']))
#         # print(r,'rrrrrrrrrrrr')
#
#         # try:
#         #     br.open(auth.authorization_url)
#         #     print(br.open(auth.authorization_url), 'first...............')
#         #     br.select_form(selector='form', nr=0)
#         #     print(br.select_form(selector='form', nr=0), 'second..............')
#         #     br['session_key'] = li_credential['un']
#         #     print(br['session_key'], 'third............')
#         #     br['session_password'] = li_credential['pw']
#         #     print(br['session_password'], 'fourth...........')
#         #     br.submit_selected()
#         #     try:
#         #         auth.authorization_code = parse_qs(urlsplit(br.get_url()).query)['code']
#         #     except:
#         #         br.open(br.get_url())
#         #         br.select_form(selector='form', nr=1)
#         #         q = br.submit_selected()
#         #         auth.authorization_code = parse_qs(urlsplit(br.get_url()).query)['code']
#         #         if not auth.authorization_code:
#         #             raise Warning("Please check Redirect URLs in the LinkedIn app settings!")
#         # except:
#         #     raise Warning("Please check gggggggggggggggRedirect URLs in the LinkedIn app settings!")
#
#         # li_suit_credent = {}
#         # li_suit_credent['access_token'] = str(auth.get_access_token().access_token)
#         # member_url = '://api.linkedin.com/v2/me'
#         # response = self.get_urn('GET', member_url, li_suit_credent['access_token'])
#         # urn_response_text = response.json()
#         # #
#         # li_credential['profile_urn'] = urn_response_text['id']
#         # #
#         # li_suit_credent['li_credential'] = li_credential
#         #
#         # return li_suit_credent
