import secrets

import requests
import webbrowser
from odoo import fields, models
import logging
from werkzeug.urls import url_encode, url_join

_logger = logging.getLogger(__name__)
# try:
#     # import mechanize
#     from linkedin_v2 import linkedin
#     # from urllib.request import HTTPRedirectHandler as MechanizeRedirectHandler
# except:
#     print('g')


class OnyxLinkedin(models.Model):
    _name = "onyx.facebook"

    client_id_facebook = fields.Char(string="Client Id")
    client_secret_facebook = fields.Char(string="Client Secret")

    # redirect_uri = fields.Char(string="Redirect uri")

    def button_facebook(self, linkedin=None):
        # urls = "https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=78us1mshswd8km" \
        #        "&redirect_uri=https://www.linkedin.com/developers/tools/oauth/redirect" \
        #        "&state=foo&scope=w_member_social,r_liteprofile,w_organization_social"
        # # print('gggggggggggggggggg')
        # authentication_url = 'https://api.linkedin.com/v2/me'
        # credentials = {
        #     'response_type': 'code',
        #     'client_id': self.client_id,
        #     'client_secret': self.client_secret,
        #     'redirect_uri': 'https://www.linkedin.com/developers/tools/oauth/redirect',
        #     'code': 'foo',
        #     'grant_type': 'authorization_code',
        #
        # }
        # print(authentication_url, 'dsffffff', credentials)
        # headers = {
        #     'Content-type': 'application/json',
        #     'Authorization': 'Bearer' + 'AQVCCNFp-ffS1h5xSnm_CVR3yMxJfMUgQDMqKZhX_t4npFuy_8AJyJsirNfF4aZ2pauTQoIbYJpz4gZxtoMYxPZ_ZIs4buhkHFfrBjk_WKeHKIiCibXp-CqdkQUpWfHQE7rqVzH5s_Lrabs_Qo938UYux_mozcEFd9NP-FtgwPTMc-Xjc0PLo-v5fofAIgJvo6ACBxitSdoLGA-4Ugcp4i3sDmSt1e2A8ccuDY_PulJSRsKzVHlgWLDJNUmXrmr31G4CynYoHqIWBSEvur7F1hWiMdGOfMD2DEXlZOh-yfX3j4cZVGIpb8KPPbUgUrp18Ku8cZV4qP0s2TAhKGZjc6Qr1ujHWA'
        # }
        # header = {
        #     'Content-type': 'application/json',
        # }
        # session = requests.Session()
        # # r = session.post(authentication_url,
        # #                  data=credentials, headers=headers)
        # # r = requests.request('GET', authentication_url,
        # #                      data=credentials, headers=headers)
        # res = requests.request('GET', urls)
        #
        #
        # print('res', urls)
        # print(res, 'rrrrrrrrrrrr')
        # print('ressssssssss',res.text)
        # # li_credential = {}
        # return webbrowser.open(urls)
        # redirect_uri = 'https://www.linkedin.com/developers/tools/oauth/redirect'

        # url = requests.Request(
        #     'GET',
        #     'https://www.linkedin.com/oauth/v2/authorization',
        #     params={
        #         'response_type': 'code',  # Always should equal to fixed string "code"
        #
        #         # ClientID of your created application
        #         'client_id': self.client_id,
        #         'redirect_uri': 'https://www.linkedin.com/developers/tools/oauth/redirect',
        #         'state': secrets.token_hex(8).upper(),
        #         'scope': 'r_liteprofile,r_emailaddress,w_member_social',
        #     },
        # ).prepare().url
        # auth_url = "https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=78us1mshswd8km" \
        #        "&redirect_uri=https://www.linkedin.com/developers/tools/oauth/redirect" \
        #        "&state=foo&scope=w_member_social,r_liteprofile,w_organization_social"

        # auth = requests.request('GET', auth_url,  params={
        #         'response_type': 'code',  # Always should equal to fixed string "code"
        #
        #         # ClientID of your created application
        #         'client_id': self.client_id,
        #         'redirect_uri': 'https://www.linkedin.com/developers/tools/oauth/redirect',
        #         'state': secrets.token_hex(8).upper(),
        #         'scope': 'r_liteprofile,r_emailaddress,w_member_social',
        #     }, headers=header)
        #
        # print(auth_url,'llllllllllllllllllllllllll')
        # # print('LLLLLLLLLLLLLLLLLLL', auth_url.text)

        params = {
            # 'response_type': 'code',
            'client_id': self.client_id_facebook,
            # 'client_secret':self.client_secret_facebook,
            'redirect_uri': self._get_facebook_redirect_uri(),
            'state': 678890,
            # 'scope': 'r_liteprofile r_emailaddress w_member_social rw_organization_admin w_organization_social r_organization_social'
        }
        print('params',params,'https://www.facebook.com/v6.0/dialog/oauth?%s' % url_encode(params))

        return {
            'type': 'ir.actions.act_url',
            'url': 'https://www.facebook.com/v6.0/dialog/oauth?%s' % url_encode(params),
        #            'https: // www.facebook.com / v6
        # .0 / dialog / oauth?client_id = clientId & redirect_uri = URLENCODE(redirectURI) & state = 987654321'
            'target': 'self'
        }

    def _get_facebook_redirect_uri(self):
        print('**********************************', url_join(self.get_base_url(), 'social_linkedins/callback'))
        return url_join(self.get_base_url(), '/social_facebook')


        # import mechanize
        # from linkedin import linkedin
        # import mechanicalsoup
        # from urllib.parse import parse_qs
        # from urllib.parse import urlsplit
        #
        # from urllib.request import HTTPRedirectHandler as MechanizeRedirectHandler
        #
        # li_credential = {}
        # br = mechanicalsoup.StatefulBrowser()
        # br.set_cookiejar(mechanize.CookieJar())
        # li_permissions = ['r_liteprofile', 'r_emailaddress', 'w_share', 'rw_company_admin', 'w_member_social']
        #
        # auth = linkedin.LinkedInAuthentication(self.client_id,
        #                                        self.client_secret,
        #                                        redirect_uri,
        #                                        li_permissions)
        # print('auth............', auth)
        # print('br............', br)
        # print('///////////////////', br.get_url())
        #
        # try:
        #     br.open(auth)
        #     br.select_form(selector='form', nr=0)
        #     br['session_key'] = li_credential['un']
        #     br['session_password'] = li_credential['pw']
        #     br.submit_selected()
        #     try:
        #         authorization_code = parse_qs(urlsplit(br.get_url()).query)['code']
        #         print('vode', authorization_code)
        #     except:
        #         br.open(br.get_url())
        #         br.select_form(selector='form', nr=1)
        #         q = br.submit_selected()
        #         auth.authorization_code = parse_qs(urlsplit(br.get_url()).query)['code']
        #         if not auth.authorization_code:
        #             raise Warning("Please check Redirect URLs in the LinkedIn app settings!!!!!!!!!!!!")
        # except:
        #     print('ppppppppppppp')
        #
        # li_suit_credent = {}
        # li_suit_credent['access_token'] = str(auth.get_access_token().access_token)
        # member_url = 'https://api.linkedin.com/v2/me'
        # response = self.get_urn('GET', member_url, li_suit_credent['access_token'])
        # urn_response_text = response.json()
        #
        # li_credential['profile_urn'] = urn_response_text['id']
        #
        # li_suit_credent['li_credential'] = li_credential
        # print('sssssssssssss', urn_response_text)
        # print('li_suit_credent', li_suit_credent)

        # return {
        #     'type': 'ir.actions.act_url',
        #     'url': 'https://www.linkedin.com/oauth/v2/authorization?%s' % url_encode(params),
        #     'target': 'self'
        # }
# ----------------------------------------------------------------------------------------------------------------------
        # # linkedin_auth_provider = self.env.ref('hr_linkedin_recruitment.provider_linkedin')
        # # if linkedin_auth_provider.client_id and linkedin_auth_provider.client_secret:
        # li_credential['api_key'] = self.client_id
        # li_credential['secret_key'] = self.client_secret
        # print(li_credential['api_key'], li_credential['secret_key'], '[[[[[[[[[[[[[')
        # else:
        #     raise ValidationError(_('LinkedIn Access Credentials are empty.!\n'
        #                             'Please fill up in Auth Provider form.'))

        # if self.env['ir.config_parameter'].sudo().get_param('recruitment.li_username'):
        #     li_credential['un'] = self.env['ir.config_parameter'].sudo().get_param('recruitment.li_username')
        #     print(li_credential['un'], 'uuuuuuuuuuuuuuuuuuuuu')
        # else:
        #     raise exceptions.Warning(_('Please fill up username in LinkedIn Credential settings.'))

        # if self.env['ir.config_parameter'].sudo().get_param('recruitment.li_password'):
        #     li_credential['pw'] = self.env['ir.config_parameter'].sudo().get_param('recruitment.li_password')
        #     print(li_credential['pw'])
        # else:
        #     raise exceptions.Warning(_('Please fill up password in LinkedIn Credential settings.'))

        # Browser Data Posting And Signing
        # br = mechanicalsoup.StatefulBrowser()
        # br.set_cookiejar(mechanize.CookieJar())
        # return_uri = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        # print(return_uri, 'iiiiiiiiiiiii')
        # li_permissions = ['r_liteprofile', 'r_emailaddress', 'w_member_social']
        # print(li_permissions)
        # auth = linkedin.LinkedInAuthentication(li_credential['api_key'],
        #                                        li_credential['secret_key'],
        #                                        return_uri,
        #                                        li_permissions)
        # print(auth, 'brrrrr')

        # session = requests.Session()
        # r = session.post(authentication_url,
        #                  data=credentials, headers=headers)
        # r = requests.request('GET',authentication_url,
        #                  data=(li_credential['api_key']))
        # print(r,'rrrrrrrrrrrr')

        # try:
        #     br.open(auth.authorization_url)
        #     print(br.open(auth.authorization_url), 'first...............')
        #     br.select_form(selector='form', nr=0)
        #     print(br.select_form(selector='form', nr=0), 'second..............')
        #     br['session_key'] = li_credential['un']
        #     print(br['session_key'], 'third............')
        #     br['session_password'] = li_credential['pw']
        #     print(br['session_password'], 'fourth...........')
        #     br.submit_selected()
        #     try:
        #         auth.authorization_code = parse_qs(urlsplit(br.get_url()).query)['code']
        #     except:
        #         br.open(br.get_url())
        #         br.select_form(selector='form', nr=1)
        #         q = br.submit_selected()
        #         auth.authorization_code = parse_qs(urlsplit(br.get_url()).query)['code']
        #         if not auth.authorization_code:
        #             raise Warning("Please check Redirect URLs in the LinkedIn app settings!")
        # except:
        #     raise Warning("Please check gggggggggggggggRedirect URLs in the LinkedIn app settings!")

        # li_suit_credent = {}
        # li_suit_credent['access_token'] = str(auth.get_access_token().access_token)
        # member_url = '://api.linkedin.com/v2/me'
        # response = self.get_urn('GET', member_url, li_suit_credent['access_token'])
        # urn_response_text = response.json()
        # #
        # li_credential['profile_urn'] = urn_response_text['id']
        # #
        # li_suit_credent['li_credential'] = li_credential
        #
        # return li_suit_credent
