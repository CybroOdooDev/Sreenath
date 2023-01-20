# -*- coding: utf-8 -*-

from odoo import _, models, fields, api
from odoo.http import request


class OnyxSocialAccount(models.Model):
    """ A social.account represents an actual account on the related social.media.
    Ex: A Facebook Page or a Twitter Account.

    These social.accounts will then be used to send generic social.posts to multiple social.accounts.
    They are also used to display a 'dashboard' of statistics on the 'Feed' view.

    Account statistic fields are 'computed' manually through the _compute_statistics method
    that is overridden by each actual social module implementations (social_facebook, social_twitter, ...).
    The statistics computation is run manually when visualizing the Feed. """

    _name = 'onyx.social.account'
    _description = 'Onyx Social Account'
    _inherits = {'utm.medium': 'utm_medium_id'}

    def _get_default_company_onyx(self):
        """When the user is redirected to the callback URL of the different media,
        the company in the environment is always the company of the current user and not
        necessarily the selected company.

        So, before the authentication process, we store the selected company in the
        user session (see <social.media>::action_add_account) to be able to retrieve it
        here.
        """
        if request and 'social_company_id' in request.session:
            company_id = request.session['social_company_id']
            if not company_id:  # All companies
                return False
            if company_id in self.env.companies.ids:
                return company_id
        return self.env.company

    onyx_active = fields.Boolean("Active", default=True)
    media_id = fields.Many2one('onyx.social.media', string="Social Media", required=True, readonly=True,
        help="Related Social Media (Facebook, Twitter, ...).", ondelete='cascade')
    onyx_media_type = fields.Selection(related='media_id.onyx_media_type')
    onyx_stats_link = fields.Char("Stats Link", compute='_compute_stats_link_onyx',
        help="Link to the external Social Account statistics")
    image = fields.Image("Image", max_width=128, max_height=128, readonly=True)
    onyx_is_media_disconnected = fields.Boolean('Link with external Social Media is broken')

    onyx_audience = fields.Integer("Audience", readonly=True,
        help="General audience of the Social Account (Page Likes, Account Follows, ...).")
    onyx_audience_trend = fields.Float("Audience Trend", readonly=True, digits=(3, 0),
        help="Percentage of increase/decrease of the audience over a defined period.")
    onyx_engagement = fields.Integer("Engagement", readonly=True,
        help="Number of people engagements with your posts (Likes, Comments, ...).")
    onyx_engagement_trend = fields.Float("Engagement Trend", readonly=True, digits=(3, 0),
        help="Percentage of increase/decrease of the engagement over a defined period.")
    onyx_stories = fields.Integer("Stories", readonly=True,
        help="Number of stories created from your posts (Shares, Re-tweets, ...).")
    onyx_stories_trend = fields.Float("Stories Trend", readonly=True, digits=(3, 0),
        help="Percentage of increase/decrease of the stories over a defined period.")
    onyx_has_trends = fields.Boolean("Has Trends?",
        help="Defines whether this account has statistics tends or not.")
    onyx_has_account_stats = fields.Boolean("Has Account Stats", default=True, required=True,
        help="""Defines whether this account has Audience/Engagements/Stories stats.
        Account with stats are displayed on the dashboard.""")
    utm_medium_id = fields.Many2one('utm.medium', string="UTM Medium", required=True, ondelete='restrict',
        help="Every time an account is created, a utm.medium is also created and linked to the account")
    company_id = fields.Many2one('res.company', 'Company', default=_get_default_company_onyx,
                                 domain=lambda self: [('id', 'in', self.env.companies.ids)],
                                 help="Link an account to a company to restrict its usage or keep empty to let all companies use it.")
    linkedin_accesstoken = fields.Char(string="Linkedin Accesstoken")

    def _compute_statistics_onyx(self):
        """ Every social module should override this method if it 'has_account_stats'.
        As the values depend on third party data, it's compute triggered manually that stores the data on the
        various stats fields (audience, engagement, stories) as well as related trends fields (if 'has_trends'). """
        pass

    def _compute_stats_link_onyx(self):
        """ Every social module should override this method.
        The 'stats_link' is an external link to the actual social.media statistics for this account.
        Ex: https://www.facebook.com/Odoo-Social-557894618055440/insights """
        for account in self:
            account.onyx_stats_link = False
        return

    def name_get(self):
        """ ex: [Facebook] Odoo Social, [Twitter] Mitchell Admin, ... """
        return [(account.id, '[%s] %s' % (account.media_id.name, account.name if account.name else '')) for account in self]

    @api.model_create_multi
    def create(self, vals_list):
        res = super(OnyxSocialAccount, self).create(vals_list)
        res._compute_statistics_onyx()
        return res

    @api.model
    def refresh_statistics(self):
        """ Will re-compute the statistics of all active accounts. """
        all_accounts = self.env['social.account'].search([('has_account_stats', '=', True)]).sudo()
        all_accounts._compute_statistics_onyx()
        return [{
            'id': account.id,
            'name': account.name,
            'onyx_is_media_disconnected': account.is_media_disconnected,
            'onyx_audience': account.audience,
            'onyx_audience_trend': account.audience_trend,
            'onyx_engagement': account.engagement,
            'onyx_engagement_trend': account.engagement_trend,
            'onyx_stories': account.stories,
            'onyx_stories_trend': account.stories_trend,
            'onyx_has_trends': account.has_trends,
            'media_id': [account.media_id.id],
            'onyx_media_type': account.media_id.media_type,
            'onyx_stats_link': account.stats_link
        } for account in all_accounts]

    def _compute_trend(self, value, delta_30d):
        return 0.0 if value - delta_30d <= 0 else (delta_30d / (value - delta_30d)) * 100

    def _filter_by_media_types(self, onyx_media_type):
        return self.filtered(lambda account: account.onyx_media_type in onyx_media_type)

    def _get_multi_company_error_message(self):
        """Return an error message if the social accounts information can not be updated by the current user."""
        if not self.env.user.has_group('base.group_multi_company'):
            return

        cids = request.httprequest.cookies.get('cids')
        if cids:
            allowed_company_ids = {int(cid) for cid in cids.split(',')}
        else:
            allowed_company_ids = {self.env.company.id}

        accounts_other_companies = self.filtered(
            lambda account: account.company_id and account.company_id.id not in allowed_company_ids)

        if accounts_other_companies:
            return _(
                'Create other accounts for %(media_names)s for this company or ask %(company_names)s to share their accounts',
                media_names=', '.join(accounts_other_companies.mapped('media_id.name')),
                company_names=', '.join(accounts_other_companies.mapped('company_id.name')),
            )
