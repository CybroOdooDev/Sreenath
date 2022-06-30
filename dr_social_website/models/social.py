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
    date = fields.Text(string='Date')
    time = fields.Char(string='Time')
    image = fields.Text(string='Image Path')
    revision_button = fields.Boolean(string='Revision Button', default=False)

    # @api.onchange('date','time')
    # def date_time(self):
    #     print('ksdhfyku')
    #     self.scheduled_date = 'self.date'
    #     print(type(self.scheduled_date))


    def time_change(self, id, time):
        social_post = self.browse(id)
        print('social',social_post, time)

        # in_time = datetime.strptime(time, "%I:%M %p")
        # out_time = datetime.strftime(in_time, "%H:%M:%S")
        # tz = pytz.timezone("Asia/Kolkata")
        # local_time = tz.localize(fields.Datetime.to_datetime(in_time))
        # utc_time = local_time.astimezone(pytz.utc)
        # print(local_time, 'local_time', utc_time)
        # social_post.scheduled_date = fields.Datetime.to_string(utc_time)

        # date_time_obj = datetime.strptime(bbb, '%y-%m-%d %H:%M:%S')

        # aaa = bbb.replace(hour=3)
        # print('bbb', bbb)
        # social_post.write({
        #     'scheduled_date': bbb
        # })
        # print('kkkkkkkkkkkkk',id,type(time),tt,'val',val)
        # aaa = self.scheduled_date.replace(hour=0)
        # print(self.scheduled_date)
        # print(aaa)
        # self.write({
        #     'scheduled_date': aaa
        # })
        # in_time = datetime.strptime(time, "%I:%M %p")
        # out_time = datetime.strftime(in_time, "%H:%M:%S")
        # print(in_time, out_time, type(out_time), 'llllllllllllllll')
        #
        # user_tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz)
        # print(user_tz, 'lllllllllll')
        # time_object = datetime.strptime(out_time, '%H:%M:%S')
        # tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz)
        # local_time = tz.localize(fields.Datetime.to_datetime(in_time))
        # utc_time = local_time.astimezone(pytz.utc)
        # print(local_time,'local_time',utc_time)
        # bbb=fields.Datetime.to_string(utc_time)
        # date_time_obj = datetime.strptime(bbb, '%y-%m-%d %H:%M:%S')
        #
        # aaa = bbb.replace(hour=3)
        # print('bbb',bbb)
        # self.write({
        #     'scheduled_date': bbb
        # })

        # input_time = (self.time).split(':')
        # hour=int(input_time[0])
        # print(self.date)
        # self.scheduled_date = self.scheduled_date.replace(hour=0, day=7, minute=00)
        # m2 = self.time
        if time != '':
            social_post.write({'time': time, 'post_method': 'scheduled'})

            in_time = datetime.strptime(time, "%I:%M %p")
            out_time = datetime.strftime(in_time, "%H:%M:%S")
            print(in_time,out_time,type(out_time),'llllllllllllllll')

            user_tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz)
            print(user_tz,'lllllllllll')
            time_object = datetime.strptime(out_time, '%H:%M:%S')
            print(type(time_object))
            print(time_object,'time_object')
            print('dsd',social_post.scheduled_date)

            # extra_time = '05:30:00'
            # scheduled_time = datetime.strptime(out_time, "%H:%M:%S")-datetime.strptime(extra_time, "%H:%M:%S")
            scheduled_time= time_object - timedelta(hours=5, minutes=30)
            print('scheduled_time',scheduled_time)
            if social_post.date :
                dates = social_post.date.split('/')
                month = dates[0]
                day = dates[1]
                year = dates[2]
                date_chosen = year + '-' + month + '-' + day
                post = date_chosen + ' ' +datetime.strftime(scheduled_time, "%H:%M:%S")
                social_post.scheduled_date = post
            else:
                today = datetime.today().strftime('%Y-%m-%d')
                post = str(today) + ' ' + datetime.strftime(scheduled_time, "%H:%M:%S")
                social_post.scheduled_date = post
            # date_today = pytz.utc.localize(time_object).astimezone(user_tz)
            # print('ppppppppppp',post)



            # time_of=datetime.datetime.strftime(date_today, "%Y-%m-%d %H:%M:%S")
            # self.scheduled_date = time_of
            # # timee= self.scheduled_date.astimezone(
            # #     pytz.timezone('UTC')).replace(tzinfo=None)
            # print(time_of,'timeeeeeeeeeee',self.scheduled_date )
            # # first_datetime = fields.Datetime.to_datetime(self.scheduled_date).replace(tzinfo=timezone(time))
            #
            # # time= datetime.strptime(self.time,"%h:%m:%s")
            # # print(time,'prrrrrrr')

            # time_string = self.time
            # time = datetime.strftime(datetime.strptime(time_string, "%I:%M %p"), "%H:%M").split(":")
            # time = datetime.strftime(datetime.strptime(time_string, "%I:%M %p"), "%H:%M").split(":")
            # time_sch=datetime.combine(self.date, time(int(time[0]), int(time[1]), 0))
            # print(time,'pp','time_sch')

            # time_string = self.time
            # print(time_string)
            # print(fields.Date.today())
            # time_list = datetime.strftime(datetime.strptime(time_string, "%I:%M %p"), "%H:%M").split(":")
            # print(time_list)
            # self.scheduled_date=datetime.combine(fields.Date.today(), time(int(time_list[0]), int(time_list[1]), 0))

            # tz = pytz.timezone(self.env.user.tz)
            # print(tz,'pppppppppp')
            # df = datetime.fromtimestamp(time)
            # print(df,'iiiiiiiiiii')
            # local_from = tz.localize(time)
            # print(local_from,'kkkkkkkkkkkkkkkk')

        # def convert_datetime_field(datetime_field, user=None):
            # dt = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
            # if user and user.tz:
            #     user_tz = user.tz
            #     if user_tz in pytz.all_timezones:
            #         old_tz = pytz.timezone('UTC')
            #         new_tz = pytz.timezone(user_tz)
            #         dt = old_tz.localize(dt).astimezone(new_tz)
            #         print(dt)
            #     else:
            #         _logger.info("Unknown timezone {}".format(user_tz))
            #datetime.strptime(time, "%I:%M %p")
            # return datetime.strftime(dt, '%d/%m/%Y %H:%M:%S')
            #0
    def image_path(self, id,name,image):
        print(self,id,image,'kkkkkkkkkkkkkkkkkkkkk')
        attach = image.strip('data:image/jpeg;base64')
        # print('print',attach)
        Attachments = self.env['ir.attachment'].create({
            'name': name,
            # 'type': 'binary',
            'datas':  attach,
            'res_model': 'social.post',
            'res_id': id,
        })
        model = self.env['social.post'].search([('id', '=', id)])
        model.image_ids = [(4, Attachments.id)]
        print(model.image_ids)
        return model.image_ids.ids

    # def test_function(self):
    #     print("Function called from xml")
    #     return "Function called.."


        # b64 = base64.b64decode(image)
        # b64_txt = b64.decode('utf-8')
        # # file = StringIO(b64_txt)
        # print(b64,'file')

    def zoom_image(self, id):
        print('hghj',id)
        post = self.browse(id)
        image = post.image_ids.ids
        print(image,'postlll',post.message)
        return image, post.message

    def approve_text(self,id):
        print(id,'iiiiiiiiiiiiiiiiiiiiiiii')
        social_post = self.browse(id)
        social_post.write({'state': 'scheduled'})
        post = self.search_count([('state', '=', 'draft')])
        print(post,'llllllllllllllllllll')
        if post == 0:
            return 'Hide text'

    def not_approve_text(self,id):
        print(id,'iiiiiiiiiiiiiiiiiiiiiiii')
        social_post = self.browse(id)
        social_post.write({'state': 'not_approved'})
        post = self.search_count([('state', '=', 'draft')])
        print(post,'pppppppppppppp')
        if post == 0:
            return 'Hide text'

    def input_date(self, id, date):
        print(id,date,'jjjjjjjjjjj')
        social_post = self.browse(id)
        if date !='':
            social_post.date = date
            dates = date.split('/')
            print(dates,dates)
            month = dates[0]
            day = dates[1]
            year = dates[2]
            print(social_post.scheduled_date,'kkkkkkkkkkkkkkkkkkkk')
            social_post.scheduled_date = year + '-' + month + '-' + day

    @api.onchange('scheduled_date')
    def time_scheduled_date(self):
        if self.post_method == 'scheduled':
            print('kkk', self.scheduled_date)
            value = str(self.scheduled_date).split(' ')

            time = datetime.strptime(value[1], "%H:%M:%S")
            original_time = time + timedelta(hours=5, minutes=30)
            self.time = datetime.strftime(original_time, "%I:%M %p")
            print(value, time, 'kkkkkkkk', original_time)
            date = value[0].split('-')
            print(date)
            day = date[2]
            month = date[1]
            year = date[0]
            self.date = month + '/' + day + '/' + year

    def delete_image(self, id, image):
        print('approval')
        social_post = self.browse(id)
        image = image.split('/')
        image_id = int(image[6])
        image_org = self.env['ir.attachment'].search([('id','=',image_id)])
        print(image_id,image_org,)
        print(social_post.image_ids,'pppppppp',social_post)
        social_post.write({'image_ids': [(3, image_id)]})
        print(social_post.image_ids,'lll')
        # if social_post.image_ids.ids:
        #     print('kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk')
        return social_post.image_ids.ids

    def delete_upload(self, id):
        social_post = self.browse(id)
        print(';;;;;;;;;;;;;;;;;;;;;;;;;;',social_post.image_ids)
        image_id = social_post.image_ids.ids[0]
        social_post.write({'image_ids': [(3, image_id)]})

    def message_content(self,id):
        print('jjjjjjjjjjjjjjjjjjjjjjjj',id)
        social_post = self.browse(id)
        return social_post.message

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
