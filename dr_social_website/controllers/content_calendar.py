# -*- coding: utf-8 -*-
# Copyright (c) 2019-Present Droggol Infotech Private Limited. (<https://www.droggol.com/>)
import pytz

from odoo import http, _
from odoo.http import request


class ContentCalendar(http.Controller):

    @http.route(['/client_name'], type='json', auth="public", website=True)
    def client_name(self, search='', **kw):
        print('yyyyyyyyyyyyyyyyyyyyyyyyyyy',kw)
        name = kw.get('client_name')
        # post = request.env['social.post'].search([('client_name', '=', name)])
        # values = {
        #     'posts': post,
        #     'name': name
        # }
        print(name,'values')
        self.content_calendar(name)
        return 'lll'

        # return request._render_template("dr_social_website.content_calendar", values)

    @http.route(['/content_calendar'], type='http', auth="public", website=True, csrf=False)
    def content_calendar(self, search='', **kw):
        user_id = request.uid
        if not request.env.user.has_group('social.group_social_manager'):
            post = request.env['social.post'].search([('client_id', '=', user_id)])
        else:
            post = request.env['social.post'].search([])
        client_name = request.env['revision.request.client'].search([])
        name = ''
        if kw.get('client_name'):
            if kw.get('client_name'):
                name = kw.get('client_name')
                # if kw.get('client_name') not in post.client_name:
                #     print('ooooooooo')
                post = request.env['social.post'].search([('client_name', '=', kw.get('client_name'))])
                print('jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj',post,kw)

            # else:
            #     post = request.env['social.post'].search([])
            # values = {
            #         'posts': post,
            #
            #     }

        # domain=''
        # if search:
        #     print('kk')
        #     post = request.env['social.post'].search([('client_name', '=', search)])
        #     values = {
        #         'posts': post,
        #         'name': search
        #
        #     }
        #     response = http.Response(template='dr_social_website.content_calendar', qcontext=values)
        #     return response.render()

        #     for srch in search.split(" "):
        #         domain = ([
        #                    ('name', 'ilike', srch),
        #
        #                    ])
        #
        #
        #     client = request.env['revision.request.client'].search(domain)
        #     # for rec in client:
        #     post=request.env['social.post'].search([('client_name', '=', client.name)])
        #     print('ooooooooooooooooooo',post,client.name,client)
        # # print(client_name,'client_name')

        users = request.env['res.users'].search([])
        for key, value in kw.items():
            if value == '':
                if isinstance(key, int):
                    post = request.env['social.post'].search([('client_id', '=', key)])
                    values = {
                        'posts': post
                    }

        print(name,'nnnnnnnnnnnnnnnnnnnnnnn',request.env['social.post'].search([],limit=1).id)
        last_id = request.env['social.post'].search([],limit=1).id
        values = {
            'posts': post,
            'docs': [x.name for x in users],
            'name': name,
            'length':len(post),
            'last_id':last_id

        }
        print(values,'fffffffffffffffff')
        return request.render("dr_social_website.content_calendar", values)

    @http.route(['/client_approval'], type='json', auth="public", website=True, csrf=False)
    def client_approval(self, **kw):
          post = request.env['social.post'].search([('client_name', '=', kw.get('client_name'))], limit=1)
          mail_values = {
            'email_from': request.env.company.email_formatted,
            'reply_to': post.client_email,
            'email_to': post.client_email,
            'subject': 'subject',
            'body_html': '<p> Hi ' + str(post.client_name)+'!'
                         'Your new batch of posts is ready for your approval!'

                            'You can access your content calendar via this link: {link to login page}'

                            'Don’t hesitate to reach out if you have any questions!'

                         '   Best regards,'

                            'OnyxMedia Team'
                            'Refer a friend and get one month for FREE!</p>',
            'is_notification': True,
            }
          mail = request.env['mail.mail'].sudo().create(mail_values)
          mail.send()

