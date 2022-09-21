# -*- coding: utf-8 -*-
################################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
# Copyright (C) 2022-TODAY Cybrosys Technologies (
# <https://www.cybrosys.com>). Author: Cybrosys Techno Solutions (
# <https://www.cybrosys.com>)
#
#    This program is free software: you can modify
#    it under the terms of the GNU Affero General Public License (AGPL) as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
################################################################################
from datetime import datetime
from werkzeug import urls
from odoo import fields, models, api, _


class VisaApproval(models.Model):
    _name = 'visa.approval'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'visa approval'

    application_date = fields.Date(string="Application Date", default=datetime.today())
    visa_application_no = fields.Many2one('visa.application', string="Visa Application no")
    expire_date = fields.Date(string="Expire Date")
    is_expired = fields.Boolean(string='Is Expired', compute='_compute_is_expired', search='_search_is_expired')
    state = fields.Selection(
        [('draft', 'Draft'), ('submit', 'Submitted'), ('approved', 'Approved'), ('expired', 'Expired'),
         ('reject', 'Rejected')], default='draft')
    name = fields.Char(string="Approval No", readonly=True, required=True, default='New')
    employee_name = fields.Many2one("hr.employee", string="Employee Name")
    visa_type = fields.Selection([
        ('tourist', 'Tourist'),
        ('immigration', 'Immigration'),
        ('student', 'Student'),
        ('work', 'Work')], string="Visa Type")
    nationality = fields.Many2one(related="employee_name.country_id", string="Nationality")
    department_id = fields.Many2one(related="employee_name.department_id", string="Department")
    profession = fields.Char(related="employee_name.job_title", string="Profession")
    passport = fields.Char(related="employee_name.passport_id", string="Passport No")
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')], related="employee_name.gender")

    @api.model
    def update_state(self):
        for rec in self.search([('expire_date', '<', fields.date.today())]):
            rec.write({'state': 'expired'})

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('visa.management') or 'New'
            result = super(VisaApproval, self).create(vals)
            return result

    def button_visa_approve(self):
        self.state = 'approved'
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        Urls = urls.url_join(base_url, 'web#id=%(id)s&model=visa.approval&view_type=form' % {'id': self.id})

        mail_content = _('Hi %s,<br>'

                         '<div style = "text-align: left; margin-top: 16px;">'
                         'Your VISA Application have been approved.<br/>'
                         'You can check further details by clicking on the button below:<br/>'
                         '<a href = "%s"'
                         'style = "padding: 5px 10px; font-size: 12px; line-height: 18px; color: #FFFFFF; '
                         'border-color:#875A7B;text-decoration: none; display: inline-block; '
                         'margin-bottom: 0px; font-weight: 400;text-align: left; vertical-align: middle; '
                         'cursor: pointer; white-space: nowrap; background-image: none; '
                         'background-color: #875A7B; border: 1px solid #875A7B; border-radius:3px;">'
                         'View</a></div>'
                         ) % \
                       (self.employee_name.name, Urls)
        email_to = self.employee_name.work_email
        main_content = {
            'subject': _('Visa Approved'),
            'body_html': mail_content,
            'email_to': email_to
        }
        mail_id = self.env['mail.mail'].create(main_content)
        mail_id.mail_message_id.body = mail_content
        mail_id.send()

    def button_visa_submit(self):
        self.state = 'submit'
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        Urls = urls.url_join(base_url, 'web#id=%(id)s&model=visa.approval&view_type=form' % {'id': self.id})

        mail_content = _('Hi,<br>'

                         '<div style = "margin-top: 16px;">'

                         'The details of visa application and further details can be viewed by '
                         'clicking on the button below:<br/>'
                         '<a href = "%s"'
                         'style = "margin-top: 16px; padding: 5px 10px; font-size: 12px; line-height: 18px; color: #FFFFFF; '
                         'border-color:#875A7B;text-decoration: none; display: inline-block; '
                         'margin-bottom: 0px; font-weight: 400;text-align: center; vertical-align: middle; '
                         'cursor: pointer; white-space: nowrap; background-image: none; '
                         'background-color: #875A7B; border: 1px solid #875A7B; border-radius:3px;">'
                         'View</a></div>'
                         ) % \
                       (Urls)
        email_to = self.employee_name.address_id.email
        main_content = {
            'subject': _('Visa Application'),
            'body_html': mail_content,
            'email_to': email_to
        }
        mail_id = self.env['mail.mail'].create(main_content)
        mail_id.mail_message_id.body = mail_content
        mail_id.send()

    def button_renew(self):
        self.write({'state': 'draft'})

    def button_reject(self):
        self.state = 'reject'
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        Urls = urls.url_join(base_url, 'web#id=%(id)s&model=visa.approval&view_type=form' % {'id': self.id})

        mail_content = _('Hi %s,<br>'

                         '<div style = "text-align: center; margin-top: 16px;">'
                         'Your VISA Application have been rejected.<br/>'
                         'You can check further details by clicking on the button below:<br/>'
                         '<a href = "%s"'
                         'style = "padding: 5px 10px; font-size: 12px; line-height: 18px; color: #FFFFFF; '
                         'border-color:#875A7B;text-decoration: none; display: inline-block; '
                         'margin-bottom: 0px; font-weight: 400;text-align: center; vertical-align: middle; '
                         'cursor: pointer; white-space: nowrap; background-image: none; '
                         'background-color: #875A7B; border: 1px solid #875A7B; border-radius:3px;">'
                         'View</a></div>'
                         ) % \
                       (self.employee_name.name, Urls)
        email_to = self.employee_name.work_email
        main_content = {
            'subject': _('Visa Rejected'),
            'body_html': mail_content,
            'email_to': email_to
        }
        mail_id = self.env['mail.mail'].create(main_content)
        mail_id.mail_message_id.body = mail_content
        mail_id.send()

    def _compute_is_expired(self):
        now = fields.Datetime.now()
        for rec in self:
            rec.is_expired = now.date() > rec.expire_date

    def _search_is_expired(self, operator, value):
        now = fields.Datetime.now()
        ids = self.env['visa.approval']._search([('expire_date', '<', now)])
        return [('id', 'in', ids)]
