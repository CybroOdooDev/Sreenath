# -*- coding: utf-8 -*-
# Copyright (c) 2019-Present Droggol Infotech Private Limited. (<https://www.droggol.com/>)
import base64
import datetime
import io

import requests
from six import StringIO
from datetime import datetime, timedelta

from odoo import models, fields, api, _
import logging
from odoo.exceptions import UserError

import pytz
from pytz import timezone
_logger = logging.getLogger(__name__)




class ResUsers(models.Model):
    _inherit = 'res.users'

    profile_key = fields.Char('Ayrshare Profile Key')

    @api.model
    def signup(self, values, token=None):
        """ signup a user, to either:
            - create a new user (no token), or
            - create a user for a partner (with token, but no user for partner), or
            - change the password of a user (with token, and existing user).
            :param values: a dictionary with field values that are written on user
            :param token: signup token (optional)
            :return: (dbname, login, password) for the signed up user
        """
        print('!@!@!@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
        print('---------------------------------------------------------')

        if token:
            # signup with a token: find the corresponding partner id
            partner = self.env['res.partner']._signup_retrieve_partner(token, check_validity=True, raise_exception=True)
            # invalidate signup token
            partner.write({'signup_token': False, 'signup_type': False, 'signup_expiration': False})

            partner_user = partner.user_ids and partner.user_ids[0] or False

            # avoid overwriting existing (presumably correct) values with geolocation data
            if partner.country_id or partner.zip or partner.city:
                values.pop('city', None)
                values.pop('country_id', None)
            if partner.lang:
                values.pop('lang', None)

            if partner_user:
                # user exists, modify it according to values
                values.pop('login', None)
                values.pop('name', None)
                partner_user.write(values)
                if not partner_user.login_date:
                    partner_user._notify_inviter()
                return (self.env.cr.dbname, partner_user.login, values.get('password'))
            else:
                # user does not exist: sign up invited user
                values.update({
                    'name': partner.name,
                    'partner_id': partner.id,
                    'email': values.get('email') or values.get('login'),
                })
                if partner.company_id:
                    values['company_id'] = partner.company_id.id
                    values['company_ids'] = [(6, 0, [partner.company_id.id])]
                partner_user = self._signup_create_user(values)
                partner_user._notify_inviter()
        else:
            # no token, sign up an external user
            values['email'] = values.get('email') or values.get('login')
            self._signup_create_user(values)


        # ayrshare_api_key = self.env['ir.config_parameter'].sudo().get_param('dr_social_website.ayrshare_api_key')
        # if ayrshare_api_key:
        #     payload = {'title': str(values.pop('name', None))}
        #     headers = {'Content-Type': 'application/json',
        #                'Authorization': 'Bearer ' + ayrshare_api_key}
        #
        #     profile = requests.post('https://app.ayrshare.com/api/profiles/profile',
        #                             json=payload,
        #                             headers=headers)
        #
        #     print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!', profile.json())
        #     profile_data = profile.json()
        #     profile_key = profile_data['profileKey']


        #
        # else:
        #     raise UserError(_(
        #         'Please contact administrator to update the Ayrshare API Key in Settings'
        #     ))

        return (self.env.cr.dbname, values.get('login'), values.get('password'))



class ResPartner(models.Model):
    _inherit = 'res.partner'

    profile_key = fields.Char('Ayrshare Profile Key')




