# -*- coding: utf-8 -*-
# Copyright (c) 2019-Present Droggol Infotech Private Limited. (<https://www.droggol.com/>)

from odoo import http, _
from odoo.http import request


class RevisionRequest(http.Controller):

    @http.route(['/revision_requests'], type='http', auth="public", website=True)
    def get_revision_request(self, **kw):
        print('-*-******--*-*-------------*-*-********************')

        post = request.env['social.post'].search([('state', '=', 'posted')], limit=1)
        print(post)
        # lines = total_products.item_ids
        # product_count = len(lines)
        # per_page = 9
        # print(lines)
        # pager = request.website.pager(url='/offer_zone', total=product_count, page=page,
        #                               step=per_page, url_args=None)
        # offset = pager['offset']
        # print(offset)
        # pricelists = lines[offset: offset + 9]
        # print(pricelists)
        values = {
            # 'date': post.calendar_date,
            # 'message': post.message,
            # 'image': post.image_ids,
            # 'feedback': 'All is Well',
            'posts': post

        }
        # print(values)
        return request.render("dr_social_website.revision_request", values)
