# -*- coding: utf-8 -*-

from odoo import models, fields, tools, api, _
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import re
from odoo.tools.translate import _
from odoo.tools import email_re, email_split


class EmailAddressType(models.Model):
    _inherit = 'account_followup.followup.line'

    html_description = fields.Html('Printed Message', translate=True, default=lambda s: _("""
    Dear %(partner_name)s,

    Exception made if there was a mistake of ours, it seems that the following amount stays unpaid. Please, take appropriate measures in order to carry out this payment in the next 8 days.

    Would your payment have been carried out after this mail was sent, please ignore this message. Do not hesitate to contact our accounting department.

    Best Regards,
                """))

    @api.constrains('html_description')
    def _check_description(self):
        for line in self:
            if line.html_description:
                try:
                    line.html_description % {'partner_name': '', 'date': '', 'user_signature': '', 'company_name': '',
                                             'amount_due': ''}
                except KeyError:
                    raise Warning(_(
                        'Your description is invalid, use the right legend or %% if you want to use the percent character.'))


class AccountFollowupReport(models.AbstractModel):
    _inherit = "account.followup.report"

    @api.model
    def _get_default_summary(self, options):
        return self._build_followup_summary_with_field('html_description', options)
