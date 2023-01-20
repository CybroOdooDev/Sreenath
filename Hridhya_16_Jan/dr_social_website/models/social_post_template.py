# -*- coding: utf-8 -*-
# Copyright (c) 2019-Present Droggol Infotech Private Limited. (<https://www.droggol.com/>)

from odoo import models, fields, api, _


class SocialPostTemplate(models.Model):
    _inherit = 'onyx.social.post.template'

    @api.constrains('message')
    def _check_message_not_empty(self):
        for post in self:
            if not post.message:
                return
