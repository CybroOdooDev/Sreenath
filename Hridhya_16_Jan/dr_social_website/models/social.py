# -*- coding: utf-8 -*-
# Copyright (c) 2019-Present Droggol Infotech Private Limited. (<https://www.droggol.com/>)
import base64
import datetime
import io

import requests
from six import StringIO
from datetime import datetime, timedelta

from odoo import models, fields, api
import logging
import pytz
from pytz import timezone
_logger = logging.getLogger(__name__)


class SocialAccount(models.Model):
    _inherit = 'onyx.social.account'

    dr_account_user_id = fields.Many2one('res.users', string='User')
    dr_partner_id = fields.Many2one(related='dr_account_user_id.partner_id', string='Public Partner', readonly=True,
                                    store=True)
    client_id = fields.Integer(string="Client Id")



class SocialPost(models.Model):
    _inherit = "onyx.social.post"

    feedback = fields.Text(string='Feedback')
    state = fields.Selection(selection_add=[
        ('not_approved', 'Not Approved')
    ], ondelete={'not_approved': 'set default'})
    date = fields.Text(string='Date')
    # time = fields.Char(string='Time')
    image = fields.Text(string='Image Path')
    revision_button = fields.Boolean(string='Revision Button', default=False)
    revision_progress = fields.Boolean(string='Revision Progress', default=False)
    client_id = fields.Integer(string='Client Id')
    client_ids = fields.Many2one('res.users', string='Client Ids')
    client_name = fields.Char(string="Client Name")
    client_email = fields.Char(string="Client Email")
    revision_open = fields.Boolean(string="Open", default=True)
    notification_delete = fields.Boolean(string="Delete", default=False)
    viewed_feedback = fields.Boolean(string="Viewed Feedback", default=False)
    gave_feedback = fields.Boolean(string="Gave Feedback", default=False)

    # @api.onchange('client_id')
    # def client_name(self):
    #     user = self.env['res.partner'].browse('client_id')
    #     self.client_name=user.name
    #     print('llllllllllllllll',self.client_name)

    def delete_posts(self, id):
        social_post = self.browse(id)
        social_post.unlink()

    def date_time_change(self, id, date_time):
        social_post = self.browse(id)
        print(id,social_post.scheduled_date,date_time)
        if date_time != '':
        #     social_post.write({'time': time, 'post_method': 'scheduled'})
        # 2022 - 07 - 28
        # 14: 34:31
        # 8: 24
        # PM
        # 27
        # July
        # 2022
            social_post.date = date_time
            in_time = datetime.strptime(date_time, "%I:%M %p %d %B %Y")
        #     out_time = datetime.strftime(in_time, "%H:%M:%S")
            user_tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz)
        #     time_object = datetime.strptime(out_time, '%H:%M:%S')
            social_post.scheduled_date= in_time - timedelta(hours=5, minutes=30)
        print('in_time', in_time,user_tz,social_post.scheduled_date)

        #     if social_post.date :
        #         dates = social_post.date.split('/')
        #         month = dates[0]
        #         day = dates[1]
        #         year = dates[2]
        #         date_chosen = year + '-' + month + '-' + day
        #         post = date_chosen + ' ' +datetime.strftime(scheduled_time, "%H:%M:%S")
        #         social_post.scheduled_date = post
        #     else:
        #         today = datetime.today().strftime('%Y-%m-%d')
        #         post = str(today) + ' ' + datetime.strftime(scheduled_time, "%H:%M:%S")
        #         social_post.scheduled_date = post

    def image_path(self, id,name,image):
        # print('oooooooooooooooooooooo',id,name,image)
        image_type = name.split('.')
        print('yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy',image_type[1])

        if(image_type[1] == 'jpeg') or (image_type[1] == 'jpg'):
            print('kkkkkkkkkkkkkkkkkkkkk')
            attach = image.strip('data:image/jpeg;base64')
            Attachments = self.env['ir.attachment'].create({
                'name': name,
                # 'type': 'binary',
                'datas':  attach,
                'res_model': 'onyx.social.post',
                'res_id': id,
            })
            model = self.env['onyx.social.post'].search([('id', '=', id)])
            model.image_ids = [(4, Attachments.id)]
            return model.image_ids.ids

        if image_type[1] == 'png':
            attach_png = image.strip('data:image/png;base64')
            Attachments = self.env['ir.attachment'].create({
                'name': name,
                # 'type': 'binary',
                'datas':  attach_png,
                'res_model': 'onyx.social.post',
                'res_id': id,
            })
            print('gggggggggggggg',{ 'name': name,
                # 'type': 'binary',
                'res_model': 'onyx.social.post',
                'res_id': id,})
            model = self.env['onyx.social.post'].search([('id', '=', id)])
            model.image_ids = [(4, Attachments.id)]
            return model.image_ids.ids

    def zoom_image(self, id):
        print('iiiiiiiiiiiiiiii',id)
        post = self.browse(id)
        image = post.image_ids.ids
        print(post,image,'ooooooooo')
        return image, post.message

    def approve_text(self,id):
        social_post = self.browse(id)
        social_post.write({'state': 'scheduled'})
        post = self.search_count([('state', '=', 'draft')])
        if post == 0:
            return 'Hide text'

    def not_approve_text(self, id):
        social_post = self.browse(id)
        social_post.write({'state': 'not_approved'})
        post = self.search_count([('state', '=', 'draft')])
        if post == 0:
            return 'Hide text'

    # def input_date(self, id, date):
    #     social_post = self.browse(id)
    #     if date !='':
    #         social_post.date = date
    #         dates = date.split('/')
    #         print(dates,dates)
    #         month = dates[0]
    #         day = dates[1]
    #         year = dates[2]
    #         social_post.scheduled_date = year + '-' + month + '-' + day

    @api.onchange('scheduled_date')
    def time_scheduled_date(self):
        if self.post_method == 'scheduled':
            print('kkk', self.scheduled_date)
            # value = str(self.scheduled_date).split(' ')

            # time = datetime.strptime(value[1], "%H:%M:%S")
            original_time = self.scheduled_date + timedelta(hours=5, minutes=30)
            self.date = datetime.strftime(original_time, "%I:%M %p %d %B %Y")
            print(self.date,'selfff')
            # date = value[0].split('-')
            # day = date[2]
            # month = date[1]
            # year = date[0]
            # self.date = month + '/' + day + '/' + year


    def delete_image(self, id, image):
        social_post = self.browse(id)
        image = image.split('/')
        image_id = int(image[6])
        image_org = self.env['ir.attachment'].search([('id','=',image_id)])
        social_post.write({'image_ids': [(3, image_id)]})
        return social_post.image_ids.ids

    def delete_upload(self, id):
        social_post = self.browse(id)
        if social_post.image_ids:
            image_id = social_post.image_ids.ids[0]
            print(social_post,image_id,'ll',social_post.image_ids)
            social_post.write({'image_ids': [(3, image_id)]})

    def message_content(self,id):
        social_post = self.browse(id)
        return social_post.message

    def load_feedback(self, id, text, user):
        print('dksdjf')
        social_post = self.browse(id)
        print(social_post,'ffffffffffffffffffffffffffffffffffffffffffffffffffff')
        social_post.feedback = text
        # social_post.client_id = user
        social_post.revision_progress = True
        social_post.gave_feedback = True
        # user_id = self.env['res.users'].search([('id', '=', user)])
        # social_post.client_name = user_id.name

    def new_post_create(self, client_name):
        client_id = self.env['res.users'].search([('name', '=', client_name)])
        print(client_id,'gggggggggggggg',{'client_name': client_name,
            'client_id': client_id.id,
            'client_email': client_id.login,})
        client_email = client_id.login
        self.create({
            'client_name': client_name,
            'client_id': client_id.id,
            'client_email': client_email,
        })

    def delete_notification_revision(self, client_id):
        post = self.search([('client_id', '=', client_id), ('revision_open', '=', True), ('gave_feedback', '=', True)])
        print('lllllllllllllllllllllllllllllllllllllllllllllllllllllllll',client_id,post)
        for rec in post:
            rec.notification_delete = True
            rec.revision_open = False
            # rec.gave_feedback = False

    def feedbacks_viewed(self, client_id):
        post = self.search([('client_id', '=', client_id), ('revision_open', '=', True), ('notification_delete', '=', False)])
        print('lllllllllllllllllllllllllllllllllllllllllllllllllllllllll',client_id,post)
        for rec in post:
            rec.viewed_feedback = True

            # rec.revision_open = False




class RevisionClientName(models.Model):
    _name = "revision.request.client"

    name = fields.Char('Client Name', copy=False)
    date_day = fields.Text(string='Day')
    date_month = fields.Text(string='Month')
    client_id = fields.Integer(string='Client Id')
    email_id = fields.Char(string='Email')

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
