"""Delivery Boy"""
# -*- coding: utf-8 -*-

# 1 : imports of odoo
from odoo import models, fields, api ,_
from odoo.exceptions import ValidationError, UserError

class ResPartner(models.Model):
    _inherit = 'stock.picking'

    delivery_boy = fields.Many2one('res.partner', string='Delivery Boy')
    delivery_boy_picking = fields.Many2one('delivery.boy', string='Delivery Boy Picking')
    is_assigned = fields.Boolean('Is Assigned?', default=False)

    def action_assign_delivery_boys(self):
        for move in self.move_ids_without_package:
            if move.product_uom_qty > move.forecast_availability:
                raise UserError(_('Delivery Boy cannot be assigned because of demand quantity is not available'))
        return {
                'type': 'ir.actions.act_window',
                'name': _('Add Delivery Boy'),
                'res_model': 'assign.delivery.boy',
                'target': 'new',
                'view_mode': 'form',
                'view_type': 'form',
                'context': {
                    'default_stock_picking_id': self.id,
                    }
                }


    def action_reassign_delivery_boys(self):
        for move in self.move_ids_without_package:
            if move.product_uom_qty > move.forecast_availability:
                raise UserError(_('Delivery Boy cannot be assigned because of demand quantity is not available'))
        return {
                'type': 'ir.actions.act_window',
                'name': _('Add Delivery Boy'),
                'res_model': 'assign.delivery.boy',
                'target': 'new',
                'view_mode': 'form',
                'view_type': 'form',
                'context': {
                    'default_stock_picking_id': self.id,
                    }
                }



