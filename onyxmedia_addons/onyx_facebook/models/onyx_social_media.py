# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import requests

from odoo import _, models, fields
from odoo.exceptions import UserError
from werkzeug.urls import url_encode, url_join

from odoo.http import request


class SocialFacebookOnyx(models.Model):
    _inherit = 'onyx.social.media'

    # _FACEBOOK_ENDPOINT = 'https://graph.facebook.com'

    onyx_media_type = fields.Selection(selection_add=[('facebook', 'Facebook')])

    def _action_add_account_onyx(self):
        """ Builds the URL to Facebook with the appropriate page rights request, then redirects the client.
        Redirect is done in 'self' since Facebook will then return back to the app with the 'redirect_uri' param.

        Redirect URI from Facebook will land on this module controller's 'facebook_account_callback' method.

        Facebook will display an error message if the callback URI is not correctly defined in the Facebook APP settings. """

        self.ensure_one()

        if self.onyx_media_type != 'facebook':
            return super(SocialFacebookOnyx, self)._action_add_account_onyx()
        # model = self.env['onyx.facebook'].sudo().search([], limit=1)
        client_id_facebook = request.env['ir.config_parameter'].sudo().get_param('onyx_facebook.client_id_facebook')
        client_secret_facebook = request.env['ir.config_parameter'].sudo().get_param('onyx_facebook.client_secret_facebook')
        print('ddddddddddddddddddddddddddd',client_id_facebook)
        params = {
            # 'response_type': 'code',
            'client_id': client_id_facebook,
            # 'client_secret':self.client_secret_facebook,
            'redirect_uri': self._get_facebook_redirect_uri(),
            'state': 678890,
            # 'scope': 'r_liteprofile r_emailaddress w_member_social rw_organization_admin w_organization_social r_organization_social'
        }
        print('params', params)

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

        # if facebook_app_id and facebook_client_secret:
        #     return self._add_facebook_accounts_from_configuration(facebook_app_id)
        # else:
        #     return self._add_facebook_accounts_from_iap()

    # def _add_facebook_accounts_from_configuration(self, facebook_app_id):
    #     base_facebook_url = 'https://www.facebook.com/v10.0/dialog/oauth?%s'
    #     params = {
    #         'client_id': facebook_app_id,
    #         'redirect_uri': url_join(self.get_base_url(), "social_facebook/callback"),
    #         'response_type': 'token',
    #         'scope': ','.join([
    #             'pages_manage_ads',
    #             'pages_manage_metadata',
    #             'pages_read_engagement',
    #             'pages_read_user_content',
    #             'pages_manage_engagement',
    #             'pages_manage_posts',
    #             'read_insights'
    #         ])
    #     }
    #
    #     return {
    #         'type': 'ir.actions.act_url',
    #         'url': base_facebook_url % url_encode(params),
    #         'target': 'self'
    #     }
    #
    # def _add_facebook_accounts_from_iap(self):
    #     social_iap_endpoint = self.env['ir.config_parameter'].sudo().get_param(
    #         'social.social_iap_endpoint',
    #         self.env['social.media']._DEFAULT_SOCIAL_IAP_ENDPOINT
    #     )
    #
    #     iap_add_accounts_url = requests.get(url_join(social_iap_endpoint, 'api/social/facebook/1/add_accounts'),
    #         params={
    #             'returning_url': url_join(self.get_base_url(), 'social_facebook/callback'),
    #             'db_uuid': self.env['ir.config_parameter'].sudo().get_param('database.uuid')
    #         },
    #         timeout=5
    #     ).text
    #
    #     if iap_add_accounts_url == 'unauthorized':
    #         raise UserError(_("You don't have an active subscription. Please buy one here: %s", 'https://www.odoo.com/buy'))
    #
    #     return {
    #         'type': 'ir.actions.act_url',
    #         'url': iap_add_accounts_url,
    #         'target': 'self'
    #     }
