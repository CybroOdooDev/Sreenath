# -*- coding: utf-8 -*-
# Copyright (c) 2019-Present Droggol Infotech Private Limited. (<https://www.droggol.com/>)

from odoo import models, fields


class SocialAccount(models.Model):

    _inherit = 'social.account'

    dr_account_user_id = fields.Many2one('res.users', string='User')
    dr_partner_id = fields.Many2one(related='dr_account_user_id.partner_id', string='Public Partner', readonly=True, store=True)

