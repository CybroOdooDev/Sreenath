"""Delivery Boy"""
# -*- coding: utf-8 -*-

# 1 : imports of odoo
from odoo import models, fields, api ,_

class ResPartner(models.Model):
    _inherit = 'res.partner'

    delivery_boy_state = fields.Selection([('delivery_boy_active', 'Active'),('delivery_boy_inactive', 'Inactive'),], string="Send Using", default='delivery_boy_inactive')

    def action_active_delivery_boys(self):
        """Active Delivery Boy"""
        for record in self:
            record.delivery_boy_state = 'delivery_boy_inactive'

    def action_inactive_delivery_boys(self):
        """Inactive Delivery Boy"""
        for record in self:
            record.delivery_boy_state = 'delivery_boy_active'
