# -*- coding: utf-8 -*-
# Copyright (c) 2019-Present Droggol Infotech Private Limited. (<https://www.droggol.com/>)

from odoo import http, _
from odoo.http import request
from odoo.addons.auth_oauth.controllers.main import fragment_to_query_string
from odoo.addons.social_facebook.controllers.main import SocialFacebookController
from odoo.addons.social_twitter.controllers.main import SocialTwitterController
from odoo.addons.social_linkedin.controllers.main import SocialLinkedinController
from odoo.addons.social_instagram.controllers.main import SocialInstagramController


class SocialFacebookControllerExt(SocialFacebookController):

    @fragment_to_query_string
    @http.route(['/social_facebook/callback'], type='http', auth='user_sudo')
    def social_facebook_account_callback(self, access_token=None, is_extended_token=False, **kw):
        result = super().social_facebook_account_callback(access_token=access_token, is_extended_token=is_extended_token, **kw)
        return self._dr_handle_redirection(result)

    def _dr_handle_redirection(self, result):
        if result and not result.qcontext.get('error_message'):
            return request.redirect('/social/home')
        return result


class SocialTwitterControllerExt(SocialTwitterController):

    @fragment_to_query_string
    @http.route('/social_twitter/callback', type='http', auth='user_sudo')
    def social_twitter_account_callback(self, oauth_token=None, oauth_verifier=None, iap_twitter_consumer_key=None, **kw):
        result = super().social_twitter_account_callback(oauth_token=oauth_token, oauth_verifier=oauth_verifier, iap_twitter_consumer_key=iap_twitter_consumer_key, **kw)
        return self._dr_handle_redirection(result)

    def _dr_handle_redirection(self, result):
        if result and not result.qcontext.get('error_message'):
            return request.redirect('/social/home')
        return result


class SocialLinkedinControllerExt(SocialLinkedinController):

    @fragment_to_query_string
    @http.route('/social_linkedin/callback', type='http', auth='user_sudo')
    def social_linkedin_callback(self, access_token=None, code=None, state=None, **kw):
        result = super().social_linkedin_callback(access_token=access_token, code=code, state=state, **kw)
        return self._dr_handle_redirection(result)

    def _dr_handle_redirection(self, result):
        if result and not result.qcontext.get('error_message'):
            return request.redirect('/social/home')
        return self._dr_handle_redirection(result)


class SocialInstagramControllerExt(SocialInstagramController):

    @fragment_to_query_string
    @http.route('/social_instagram/callback', type='http', auth='user_sudo')
    def social_instagram_callback(self, access_token=None, extended_access_token=None, **kw):
        result = super().social_instagram_callback(access_token=access_token, extended_access_token=extended_access_token, **kw)
        return self._dr_handle_redirection(result)

    def _dr_handle_redirection(self, result):
        if result and not result.qcontext.get('error_message'):
            return request.redirect('/social/home')
        return self._dr_handle_redirection(result)
