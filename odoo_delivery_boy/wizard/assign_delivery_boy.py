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
import urllib.parse as parse
from twilio.rest import Client


class AssignDeliveryBoy(models.TransientModel):
    """
    This function helps to add a delivery boy to a customer.
    """
    _name = 'assign.delivery.boy'

    def _get_delivery_boys(self):
        domain = [('id', '=', -1)]
        employee_list=[]
        res_partner = self.env['res.partner'].search([]).filtered(lambda x:x.delivery_boy_state == 'delivery_boy_active')
        print('!!!!!!!!!!', res_partner)
        for each in res_partner:
            employee_list.append(each.id)
        if employee_list:
            domain =[('id', 'in', employee_list)]
            return domain
        return domain
    partner_id = fields.Many2one('res.partner', required=True, domain=_get_delivery_boys)
    stock_picking_id = fields.Many2one('stock.picking', string='Pickings')



    def add_delivery_boy(self):
        print(('add_delivery_boy', self.partner_id))
        if self.stock_picking_id.state not in ['done', 'cancel']:
            if not self.stock_picking_id.is_assigned:
                deliver_pickings = self.env['delivery.boy'].create({
                    'name': self.env['ir.sequence'].next_by_code(
                    'delivery.boy') or _('New'),
                    'assigned_date': self.stock_picking_id.scheduled_date,
                    'commission_date': self.stock_picking_id.scheduled_date,
                    'sale_order_id': self.stock_picking_id.sale_id.id,
                    'stock_picking_id': self.stock_picking_id.id,
                    'partner_id': self.partner_id.id,
                    'commission_amount': '10',
                })
                self.stock_picking_id.delivery_boy_picking = deliver_pickings.id
                self.stock_picking_id.delivery_boy = self.partner_id.id
                self.stock_picking_id.is_assigned = True
            else:
                deliver_pickings = self.stock_picking_id.delivery_boy_picking.update({ 'partner_id': self.partner_id.id, })
                self.stock_picking_id.delivery_boy = self.partner_id.id

        return deliver_pickings
