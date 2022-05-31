# -*- coding: utf-8 -*-
# Copyright (c) 2019-Present Droggol Infotech Private Limited. (<https://www.droggol.com/>)

from odoo import http, _
from odoo.http import request


class ContentCalendar(http.Controller):

    @http.route(['/content_calendar'], type='http', auth="public", website=True)
    def content_calendar(self, **kw):
        print('hiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii')

        post = request.env['social.post'].search([('state', '=', 'posted')])
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
        return request.render("dr_social_website.content_calendar", values)

