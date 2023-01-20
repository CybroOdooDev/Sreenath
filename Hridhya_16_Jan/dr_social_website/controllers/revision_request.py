# -*- coding: utf-8 -*-
# Copyright (c) 2019-Present Droggol Infotech Private Limited. (<https://www.droggol.com/>)

from odoo import http, _
from odoo.http import request


class RevisionRequest(http.Controller):

    @http.route(['/revision_requests'], type='http', auth="public", website=True)
    def get_revision_request(self, **kw):

        query = '''
        select client_id, client_name,viewed_feedback ,count(notification_delete) from onyx_social_post where notification_delete=False and gave_feedback=True group by client_id, client_name,viewed_feedback

        '''

        request._cr.execute(query)
        records = request._cr.dictfetchall()
        client_idss = []
        client_names = []
        for rec in records:
            client_idss.append(rec['client_id'])
            client_names.append(rec['client_name'])
        client_ids = [*set(client_idss)]
        client_name = [*set(client_names)]
        queries = '''select client_id, client_name, count(notification_delete) from onyx_social_post where notification_delete=False and gave_feedback=True group by client_id, client_name
                '''
        request._cr.execute(queries)
        record = request._cr.dictfetchall()
        counts = []

        for recs in record:
            counts.append(recs['count'])

        print('recordsrecordsrecordsrecords', records)
        # print(client_ids,'client_ids')
        # for rec in records:
        #      print(rec)
        #      social = request.env['social.post'].search([('viewed_feedback', '=', True),('client_id', '=', rec['client_id']),('notification_delete', '=', False),('gave_feedback', '=', True),
        #                                                  ('client_name', '=', rec['client_name'])])
        #
        #      for posts in social:
        #          post = posts.viewed_feedback
        #      print('sssssssss',[rec] + [post], [rec].append([post]))
        #          # for val in rec:
        #          #      print(val,'llllllllllllllllllllllppppppp')
        #          # print(rec.append(post),'lkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk')
        # # print([rec] + [post],'lllllllllllllllllldddddddddddddddd')
        # # records.append(post)
        # print(social, 'social')
        values = {
            'posts': records,
        }
        return request.render("dr_social_website.revision_request", values)
