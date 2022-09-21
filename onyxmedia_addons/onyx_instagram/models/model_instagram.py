import secrets

import requests
import webbrowser
from odoo import fields, models
import logging
from werkzeug.urls import url_encode, url_join

_logger = logging.getLogger(__name__)

class OnyxInstagram(models.Model):
    _name = "onyx.instagram"

    client_id_instagram = fields.Char(string="Client Id")
    client_secret_instagram = fields.Char(string="Client Secret")

    def button_instagram(self):
        params = {

            'client_id': self.client_id_instagram,
            'redirect_uri': 'https://cybroodoodev-demo-repo.odoo.com/social_instagram',

            'scope': 'user_profile,user_media',
            'response_type': 'code',
            # 'scope': 'r_liteprofile r_emailaddress w_member_social rw_organization_admin w_organization_social r_organization_social'
        }
        print('params', params)
        return {
            'type': 'ir.actions.act_url',
            'url': 'https://api.instagram.com/oauth/authorize?%s' % url_encode(params),
            'target': 'self'
        }

    def _get_instagram_redirect_uri(self):
        return url_join(self.get_base_url(), '/social_instagram')


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
