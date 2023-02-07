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

class StockWhatsapp(models.Model):
    _inherit = 'stock.picking'

    def delivery_whatsapp(self):
        '''
        This module helps to send whatsapp message to the customer from the delivery.
        When you click the button, it will open a wizard that conatain the message to
        send to the whatsapp web page.
        '''
        if not self.partner_id.mobile:
            context_record = dict(self._context or {})
            context_record['whatsapp_message'] = "Add whatsapp mobile number in sale order partner!"
            return {
                'name': 'Whatsapp Mobile Number Field is Empty',
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'number.warning.message',
                'views': [(self.env.ref('whatsapp_integration_odoo.warning_message_wizard_view').id, 'form')],
                'view_id': self.env.ref('whatsapp_integration_odoo.warning_message_wizard_view').id,
                'target': 'new',
                'context': context_record
            }

        if not self.partner_id.mobile[0] == "+":
            context_record = dict(self._context or {})
            context_record['whatsapp_message'] = "Please add a valid mobile number along with a valid country code!"
            return {
                'name': 'Invalid Mobile Number',
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'number.warning.message',
                'views': [((self.env.ref('whatsapp_integration_odoo.warning_message_wizard_view')).id, 'form')],
                'view_id': (self.env.ref('whatsapp_integration_odoo.warning_message_wizard_view')).id,
                'target': 'new',
                'context': context_record
            }
        else:
            return {'type': 'ir.actions.act_window',
                    'name': _('Whatsapp Message'),
                    'res_model': 'send.message.wizard',
                    'target': 'new',
                    'view_mode': 'form',
                    'view_type': 'form',
                    'context': {
                        'default_mail_template_id': self.env.ref('whatsapp_integration_odoo.whatsapp_template_for_delivery').id},
                    }