# -*- coding: utf-8 -*-

from odoo import fields, models
from odoo.http import request
from odoo.tools import hmac


class OnyxSocialMedia(models.Model):
    """ A social.media represents the actual Media, ex: Facebook, Twitter, etc...
    As opposed to social.account that represents an existing account on this media.
    Ex: Odoo Social Facebook Page, Mitchell Admin Twitter Account, ...

    The social.media is used to store global media configuration (API keys, ...).
    It's also used to install the modules related to that social media (social_facebook, social_twitter, ...). """

    _name = 'onyx.social.media'
    _description = 'Onyx Social Media'
    _inherit = ['mail.thread']

    _DEFAULT_SOCIAL_IAP_ENDPOINT = 'https://social.api.odoo.com'

    name = fields.Char('Name', readonly=True, required=True, translate=True)
    onyx_media_description = fields.Char('Description', readonly=True)
    image = fields.Binary('Image', readonly=True)
    onyx_media_type = fields.Selection([], readonly=True,
        help="Used to make comparisons when we need to restrict some features to a specific media ('facebook', 'twitter', ...).")
    csrf_token = fields.Char('CSRF Token', compute='_compute_csrf_token_onyx',
        help="This token can be used to verify that an incoming request from a social provider has not been forged.")
    onyx_account_ids = fields.One2many('onyx.social.account', 'media_id', string="Social Accounts")
    onyx_accounts_count = fields.Integer('# Accounts', compute='_compute_accounts_count_onyx')
    onyx_has_streams = fields.Boolean('Streams Enabled', default=True, readonly=True, required=True,
        help="Controls if social streams are handled on this social media.")
    onyx_can_link_accounts = fields.Boolean('Can link accounts ?', default=True, readonly=True, required=True,
        help="Controls if we can link accounts or not.")
    # onyx_stream_type_ids = fields.One2many('social.stream.type', 'onyx_media_id', string="Stream Types")

    def _compute_accounts_count_onyx(self):
        for media in self:
            media.onyx_accounts_count = len(media.onyx_account_ids)

    def _compute_csrf_token_onyx(self):
        for media in self:
            media.csrf_token = hmac(self.env(su=True), 'social_social-account-csrf-token', media.id)

    def action_add_account_onyx(self, company_id=None):
        print('dhfsjgjsdzfzdf')
        # Set the company of the futures new accounts (see <social.account>::_get_default_company)
        if company_id is None:
            company_id = self.env.company.id
        request.session['social_company_id'] = company_id
        return self._action_add_account_onyx()

    def _action_add_account_onyx(self):
        print('hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh')
        """ Every social module should override this method.
        Usually redirects to the social media links that allows accounts to be read by our app. """
        pass
