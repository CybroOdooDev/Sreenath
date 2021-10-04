# -*- coding: utf-8 -*-

from odoo import models, fields, tools, api, _
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import re
from odoo.tools.translate import _
from odoo.tools import email_re, email_split


class EmailAddressType(models.Model):
    _name = 'email.address.type'

    name = fields.Char('Name')
    default_to = fields.Char('Default To')


class EmailAddressInstance(models.Model):
    _name = 'email.address.instance'

    type = fields.Many2one('email.address.type', 'Types')
    contact = fields.Many2one('res.partner', 'Contacts')
    address = fields.Char('Address')


class Partner(models.Model):
    _inherit = 'res.partner'

    email_address_instance = fields.One2many('email.address.instance', 'contact', string='Email Addresses')


class MailTemplate(models.Model):
    _inherit = 'mail.template'

    email_to_use = fields.Many2one('email.address.type', string='Email Type To Use')

    @api.onchange('email_to_use')
    def action_email_to_use(self):
        emails = []
        for rec in self:
            if rec.email_to_use:
                instance = self.env['email.address.instance'].search([('type', '=', rec.email_to_use.id)])
                for ins in instance:
                    emails.append(ins.address)
                emails = set(emails)
                set_email = ','.join(emails)
                rec.email_to = set_email
            else:
                rec.email_to = rec.email_to


class MailComposeMessage(models.TransientModel):
    _inherit = 'mail.compose.message'

    email_to_use = fields.Many2one('email.address.type', string='Email Type To Use')

    @api.onchange('email_to_use')
    def action_email_to_use(self):
        contacts = []
        for rec in self:
            if rec.email_to_use:
                instance = self.env['email.address.instance'].search([('type', '=', rec.email_to_use.id)])
                for ins in instance:
                    contacts.append(ins.contact.id)
                self.partner_ids = rec.partner_ids.ids + contacts
