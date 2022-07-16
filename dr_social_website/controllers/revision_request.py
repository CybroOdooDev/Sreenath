# -*- coding: utf-8 -*-
# Copyright (c) 2019-Present Droggol Infotech Private Limited. (<https://www.droggol.com/>)

from odoo import http, _
from odoo.http import request


class RevisionRequest(http.Controller):

    @http.route(['/revision_requests'], type='http', auth="public", website=True)
    def get_revision_request(self, **kw):

        query = '''select rs.name,sc.client_id,count(sc.id) from social_post as sc, res_users as ru, res_partner as rs where
        ru.id = sc.create_uid and rs.id = ru.partner_id group by sc.create_uid, ru.login, rs.name, sc.client_id'''
        request._cr.execute(query)
        records = request._cr.dictfetchall()
        print(records,'eeeeeeeeeeeeeeeeeeeeeeeeee')

        values = {
            'posts': records,
        }
        return request.render("dr_social_website.revision_request", values)
