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

    def generate_recipients(self, results, res_ids):
        """Generates the recipients of the template. Default values can ben generated
        instead of the template values if requested by template or context.
        Emails (email_to, email_cc) can be transformed into partners if requested
        in the context. """
        self.ensure_one()

        if self.use_default_to or self._context.get('tpl_force_default_to'):
            records = self.env[self.model].browse(res_ids).sudo()
            default_recipients = records._message_get_default_recipients()
            for res_id, recipients in default_recipients.items():
                results[res_id].pop('partner_to', None)
                results[res_id].update(recipients)

        records_company = None
        if self._context.get('tpl_partners_only') and self.model and results and 'company_id' in self.env[
            self.model]._fields:
            records = self.env[self.model].browse(results.keys()).read(['company_id'])
            records_company = {rec['id']: (rec['company_id'][0] if rec['company_id'] else None) for rec in records}

        for res_id, values in results.items():
            partner_ids = values.get('partner_ids', list())
            if self._context.get('tpl_partners_only'):
                mails = tools.email_split(values.pop('email_to', '')) + tools.email_split(values.pop('email_cc', ''))
                Partner = self.env['res.partner']
                if records_company:
                    Partner = Partner.with_context(default_company_id=records_company[res_id])
                for mail in mails:
                    partner = Partner.find_or_create(mail)
                    partner_ids.append(partner.id)
            partner_to = values.pop('partner_to', '')
            type_partners = self.env['res.partner']

            if partner_to:
                # placeholders could generate '', 3, 2 due to some empty field values
                tpl_partner_ids = [int(pid) for pid in partner_to.split(',') if pid]
                partner_ids += self.env['res.partner'].sudo().browse(tpl_partner_ids).exists().ids
                for part in type_partners.search([('id', '=', partner_to)]):
                    if self.email_to_use in part.email_address_instance.type:
                        for instance in part.email_address_instance:
                            if self.email_to_use == instance.type:
                                add_partners = type_partners.find_or_create(instance.address)
            partner_ids += add_partners.ids

            results[res_id]['partner_ids'] = partner_ids
        return results


class MailComposeMessage(models.TransientModel):
    _inherit = 'mail.compose.message'

    email_to_use = fields.Many2one('email.address.type', string='Email Type To Use')

    @api.onchange('email_to_use')
    def action_email_to_use(self):
        contacts = []
        for rec in self:
            if rec.email_to_use:
                type_partners = self.env['res.partner']
                for part in type_partners.search([('id', 'in', rec.partner_ids.ids)]):
                    if rec.email_to_use in part.email_address_instance.type:
                        for instance in part.email_address_instance:
                            if rec.email_to_use == instance.type:
                                add_partners = type_partners.find_or_create(instance.address)
                                contacts.append(add_partners.id)
                rec.partner_ids = rec.partner_ids.ids + contacts
