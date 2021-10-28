from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class DeliveryReturn(models.TransientModel):
    _name = 'delivery.return.wizard'

    product_id = fields.Many2one('product.product')
    qty_return = fields.Float()
    reason = fields.Char()

    @api.constrains('qty_return')
    def _check_value(self):
        qty_reserved = self.env['stock.move.line'].browse(self.env.context.get('active_id')).product_uom_qty
        if self.qty_return > qty_reserved:
            raise ValidationError(
                _('Quantity return must be less than or equal to quantity reserved'))

    def action_confirm(self):
        move_line = self.env['stock.move.line'].browse(self.env.context.get('active_id'))
        picking = self.env['stock.picking'].browse(move_line.picking_id.id)
        picking_type_id = self.env.ref('wagon_basket_delivery.delivery_return_operation_type')
        if picking.delivery_return_id and picking.delivery_return_id.state == 'draft':
            picking.delivery_return_id.write({
                'move_ids_without_package': [(0, 0, {
                    'name': self.product_id.name,
                    'product_id': self.product_id.id,
                    'product_uom': self.product_id.uom_id.id,
                    'location_id': picking.location_id.id,
                    'location_dest_id': picking_type_id.default_location_dest_id.id,
                    'quantity_done': self.qty_return,
                    'reason': self.reason
                })],
            })
        else:
            delivery_return = self.env['stock.picking'].create({
                'picking_type_id': picking_type_id.id,
                'location_id': picking_type_id.default_location_src_id.id,
                'location_dest_id': picking_type_id.default_location_dest_id.id,
                'origin': picking.origin if picking.origin else picking.name,
                'move_ids_without_package': [(0, 0, {
                    'name': self.product_id.name,
                    'product_id': self.product_id.id,
                    'product_uom': self.product_id.uom_id.id,
                    'location_id': picking.location_id.id,
                    'quantity_done': self.qty_return,
                    'reason': self.reason
                })],
            })
            picking.delivery_return_id = delivery_return.id
        move_line.write({
            'qty_done': move_line.product_uom_qty - self.qty_return,
        })