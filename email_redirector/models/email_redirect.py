# -*- coding: utf-8 -*-

from odoo import models, fields, tools, api, _
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import re
from odoo.tools.translate import _
from odoo.tools import email_re, email_split


class EmailRedirect(models.Model):
    _name = 'email.redirect'

    regex = fields.Text('Regex')
    company_id = fields.Many2one('res.company', 'Company')


class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    @api.model
    def create(self, vals_list):
        redirect_mail = self.env['email.redirect'].search([])
        partner_details = self.env['res.partner']
        for re_mail in redirect_mail:
            mail_messages = self.env['mail.message'].search([('res_id', '=', (max(self.search([])).id))])
            for mail in mail_messages:
                if re_mail.regex:
                    regex = re_mail.regex
                    for email in email_split(mail.body):
                        searchs = re.search(regex, email)
                        if searchs:
                            find_partner = partner_details.search([('email', '=', email)])
                            if vals_list['partner_id']:
                                for part in find_partner:
                                    vals_list['partner_id'] = part.id

        return super(HelpdeskTicket, self).create(vals_list)

    def write(self, vals_list):
        redirect_mail = self.env['email.redirect'].search([])
        partner_details = self.env['res.partner']
        for re_mail in redirect_mail:
            mail_messages = self.env['mail.message'].search([('res_id', '=', self.id)])
            for mail in mail_messages:
                if re_mail.regex:
                    regex = re_mail.regex
                    for email in email_split(mail.body):
                        if tools.email_normalize(email):
                            searchs = re.search(regex, email)
                            if searchs:
                                find_partner = partner_details.search([('email', '=', email)])
                                if not self.partner_id:
                                    for part in find_partner:
                                        if self.partner_id:
                                            self.update({
                                                'partner_id': part.id
                                            })
                                        else:
                                            vals_list['partner_id'] = part.id

        return super(HelpdeskTicket, self).write(vals_list)
