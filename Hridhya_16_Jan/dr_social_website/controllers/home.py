# -*- coding: utf-8 -*-
# Copyright (c) 2019-Present Droggol Infotech Private Limited. (<https://www.droggol.com/>)

from odoo import http
from odoo.addons.web.controllers import main
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.addons.survey.wizard import survey_invite

# class Home(main.Home):

#     @http.route()
#     def index(self, *args, **kw):
#         if request.session.uid and not request.env['res.users'].sudo().browse(request.session.uid).has_group('base.group_user'):
#             return request.redirect_query('/social/home', query=request.params)
#         return super(Home, self).index(*args, **kw)

#     def _login_redirect(self, uid, redirect=None):
#         if not redirect and not request.env['res.users'].sudo().browse(uid).has_group('base.group_user'):
#             redirect = '/social/home'
#         return super(Home, self)._login_redirect(uid, redirect=redirect)


class SocialCustomerPortal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'social_count' in counters:
            values['onyx.social_count'] = request.env['onyx.social.account'].search_count([('dr_account_user_id', '=', request.env.uid)])
        return values


class Home(main.Home):

    @http.route()
    def index(self, *args, **kw):

        if request.session.uid and not request.env.user.has_group('base.group_user'):
            partner_id = request.env.user.partner_id
            if partner_id.dr_survey_id and partner_id.dr_survey_id.state != 'done':
                redirect = partner_id.dr_survey_id.get_start_url()
                return request.redirect_query(redirect, query={})

        if request.session.uid and not request.env.user.has_group('base.group_user'):
            return request.redirect_query('/social/home', query=request.params)

        return super(Home, self).index(*args, **kw)

    def _login_redirect(self, uid, redirect=None):

        is_backend_user = request.env['res.users'].sudo().browse(uid).has_group('base.group_user')
        partner_id = request.env['res.users'].sudo().browse(uid).partner_id
        if not is_backend_user and request.website.dr_survey_id and not partner_id.dr_survey_id:
            survey_user_input = request.website.dr_survey_id.sudo()._create_answer(partner=partner_id, check_attempts=False)
            partner_id.dr_survey_id = survey_user_input.id

        if partner_id.dr_survey_id and partner_id.dr_survey_id.state != 'done':
            redirect = partner_id.dr_survey_id.get_start_url()

        if not redirect and not is_backend_user:
            redirect = '/social/home'

        return super(Home, self)._login_redirect(uid, redirect=redirect)
