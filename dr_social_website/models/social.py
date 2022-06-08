# -*- coding: utf-8 -*-
# Copyright (c) 2019-Present Droggol Infotech Private Limited. (<https://www.droggol.com/>)
import base64
from datetime import datetime, time
import io

import requests
from six import StringIO

from odoo import models, fields, api
import logging
import pytz
from pytz import timezone
_logger = logging.getLogger(__name__)


class SocialAccount(models.Model):
    _inherit = 'social.account'

    dr_account_user_id = fields.Many2one('res.users', string='User')
    dr_partner_id = fields.Many2one(related='dr_account_user_id.partner_id', string='Public Partner', readonly=True,
                                    store=True)


class SocialPost(models.Model):
    _inherit = "social.post"

    feedback = fields.Text(string='Feedback')
    state = fields.Selection(selection_add=[
        ('not_approved', 'Not Approved')
    ], ondelete={'not_approved': 'set default'})
    date = fields.Date(string='Date')
    time = fields.Text(string='Time')
    image = fields.Text(string='Image Path')

    # # @api.onchange('time')
    # def time_change(self):
    #
    #     m2 = self.time
    #     in_time = datetime.strptime(m2, "%i:%m %p")
    #     out_time = datetime.strftime(in_time, "%H:%M")
    #     self.scheduled_date = str(self.date)+' '+str(out_time)+':00'
    #     user_tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz)

    def image_path(self, id,name,image):
        attach = image.strip('data:image/jpeg;base64')
        Attachments = self.env['ir.attachment'].create({
            'name': name,
            'datas':  attach,
            'res_model': 'social.post',
            'res_id': id,
        })
        model = self.env['social.post'].search([('id', '=', id)])
        model.image_ids = [(4, Attachments.id)]

