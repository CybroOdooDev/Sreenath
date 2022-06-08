# -*- coding: utf-8 -*-
# Copyright (c) 2019-Present Droggol Infotech Private Limited. (<https://www.droggol.com/>)

from odoo import http, _
from odoo.http import request


class ContentCalendar(http.Controller):

    @http.route(['/content_calendar'], type='http', auth="public", website=True)
    def content_calendar(self, **kw):
        post = request.env['social.post'].search([('state', '!=', 'posted')])
        values = {
            'posts': post
        }
        return request.render("dr_social_website.content_calendar", values)
