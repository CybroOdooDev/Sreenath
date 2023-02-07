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
import html2text
import urllib.parse as parse

class MessageError(models.TransientModel):
    _name='display.error.message'

    def get_message(self):
        '''
        This method is used to get the error message.
        :return:
        '''
        if self.env.context.get("message", False):
            return self.env.context.get('message')
        return False
    name = fields.Text(string="Message", readonly=True, default=get_message)

class SendMessage(models.TransientModel):
    _name = 'send.message.wizard'

    sale_user_id = fields.Many2one('res.partner', string="Partner Name", default=lambda self: self.env[self._context.get('active_model')].browse(self.env.context.get('active_ids')).partner_id)
    whatsapp_mobile_number = fields.Char(related='sale_user_id.mobile', required=True)
    whatsapp_message = fields.Text(string="Whatsapp Message")

    def send_custom_message(self):
        if self.whatsapp_message and self.whatsapp_mobile_number:
            message_string = parse.quote(self.whatsapp_message)
            message_string = message_string[:(len(message_string) - 3)]
            number = self.sale_user_id.mobile
            link = "https://web.whatsapp.com/send?phone=" + number
            send_msg = {
                'type': 'ir.actions.act_url',
                'url': link + "&text=" + message_string,
                'target': 'new',
                'res_id': self.id,
            }
            return send_msg