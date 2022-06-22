# -*- coding: utf-8 -*-
# Copyright (c) 2019-Present Droggol Infotech Private Limited. (<https://www.droggol.com/>)
import base64
from datetime import datetime, time
import io

import requests
from six import StringIO
import datetime
from datetime import timedelta

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


class RevisionClientName(models.Model):
    _name = "revision.request.client"

    name = fields.Char('Client Name', copy=False)
    date_day = fields.Text(string='Day')
    date_month = fields.Text(string='Month')

    @api.model
    def client_name(self, name, day, date):
        print('name', name)
        print('day', day)
        print('date', date)
        values = self.create({
            'name': name,
            'date_day': day,
            'date_month': date,
        })

        return name, day, date


class SocialPost(models.Model):
    _inherit = "social.post"

    feedback = fields.Text(string='Feedback')
    state = fields.Selection(selection_add=[
        ('not_approved', 'Not Approved')
    ], ondelete={'not_approved': 'set default'})
    date = fields.Date(string='Date')
    time = fields.Char(string='Time')
    image = fields.Text(string='Image Path')

    def time_change(self, id, time):
        social_post = self.browse(id)
        social_post.write({'time': time, 'post_method': 'scheduled'})

        in_time = datetime.strptime(time, "%I:%M %p")
        out_time = datetime.strftime(in_time, "%H:%M:%S")

        user_tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz)
        time_object = datetime.strptime(out_time, '%H:%M:%S')
        scheduled_time = time_object - timedelta(hours=5, minutes=30)
        if social_post.date:
            post = str(social_post.date) + ' ' + datetime.strftime(scheduled_time, "%H:%M:%S")
            social_post.scheduled_date = post
        else:
            today = datetime.today().strftime('%Y-%m-%d')
            post = str(today) + ' ' + datetime.strftime(scheduled_time, "%H:%M:%S")
            social_post.scheduled_date = post

    def image_path(self, id, name, image):
        attach = image.strip('data:image/jpeg;base64')
        Attachments = self.env['ir.attachment'].create({
            'name': name,
            # 'type': 'binary',
            'datas': attach,
            'res_model': 'social.post',
            'res_id': id,
        })
        model = self.env['social.post'].search([('id', '=', id)])
        model.image_ids = [(4, Attachments.id)]

    @api.onchange('scheduled_date')
    def time_scheduled_date(self):
        if self.post_method == 'scheduled':
            value = str(self.scheduled_date).split(' ')
            self.date = value[0]
            time = datetime.strptime(value[1], "%H:%M:%S")
            original_time = time + timedelta(hours=5, minutes=30)
            self.time = datetime.strftime(original_time, "%I:%M %p")
