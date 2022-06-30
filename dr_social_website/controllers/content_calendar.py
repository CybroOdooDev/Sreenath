# -*- coding: utf-8 -*-
# Copyright (c) 2019-Present Droggol Infotech Private Limited. (<https://www.droggol.com/>)
import pytz

from odoo import http, _
from odoo.http import request


class ContentCalendar(http.Controller):

    @http.route(['/content_calendar'], type='http', auth="public", website=True)
    def content_calendar(self, **kw):

        post = request.env['social.post'].search([])
        print(post)
        # user = request.uid
        # user_tz = pytz.timezone(request.env.context.get('tz') or request.env.user.tz)
        # print(user,'user_tz',user_tz)
        #
        #
        # # print(post.read(),'images')
        # # print(post.media_ids,'images')

        values = {
            'posts': post
        }
        return request.render("dr_social_website.content_calendar", values)

    @http.route(['/client_approval'], type='http', auth="public", website=True, csrf=False)
    def client_approval(self, **kw):
        print('dddddddddddddddddddd')
        template_id = request.env.ref('dr_social_website.mail_template_client_approval')
        # template = request.env['mail.template'].browse(template_id)
        template_id.send_mail(template_id.id, force_send=True)
            # send_mail(
            # self.id, force_send=True)

    # template_id = request.env.ref(
    #     'portal_user_join_invitation_website.mail_template_signup_invitation_internal').id
    # template = request.env['mail.template'].browse(template_id)
    # new_request_id = request.env.user.invited_user_ids.mapped('id')[-1]
    # template.send_mail(new_request_id, force_send=True)

    # @http.route('/submit', method='post', type='http', auth='public',
    #             website=True, csrf=False)
    # def send_request(self, **post):
    #     print('hhhdjhfhg',post)
    #     value ={
    #             'feedback': post['feedback'],
    #         }
    #     print(value,'vvvvvvvvvvvvvvvvv')
        # post= request.env['social.post'].sudo().write(
        #    value)
        # post= request.env['social.post'].sudo().update(
        #    value)

    # @http.route('/approve_button', method='post', type='http', auth='public',
    #             website=True, csrf=False)
    # def approve_button(self):
    #     post = request.env['social.post'].search([])
    #     print(post)
    #     print('llllllllllllll'/client_approval)