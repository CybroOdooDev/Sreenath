# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2021-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Cybrosys Techno Solutions(<https://www.cybrosys.com>)
#
#    You can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import html2text


class SaleOrderWhatsapp(models.Model):
    _inherit = 'sale.order'

    def sale_order_whatsapp(self):
        '''
        This module helps to send whatsapp message to the customer from the sale order.
        When you click the button, it will open a wizard that conatain the message to send to the whatsapp web page.
        '''
        if not self.partner_id.mobile:
            raise ValidationError(_("Add whatsapp mobile number in sale order partner!"))

        if not self.partner_id.mobile[0] == "+":
            raise ValidationError(_("Please add a valid mobile number along with a valid country code!"))

        else:
            template_id = self.env.ref('whatsapp_integration_odoo.whatsapp_template_for_sale_order').id
            mail_template_values = self.env['mail.template'].with_context(tpl_partners_only=True).browse(
                template_id).generate_email([self.id], fields=['body_html'])
            body_html = dict(mail_template_values)[self.id].pop('body_html', '')
            whatsapp_message = html2text.html2text(body_html)
            return {'type': 'ir.actions.act_window',
                    'name': _('Whatsapp Message'),
                    'res_model': 'send.message.wizard',
                    'target': 'new',
                    'view_mode': 'form',
                    'view_type': 'form',
                    'context': {
                        'default_whatsapp_message': whatsapp_message},
                    }