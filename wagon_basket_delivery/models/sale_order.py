from odoo import models, fields, api, _
from odoo.tools.float_utils import float_compare, float_is_zero, float_round


class SaleOrder(models.Model):
    _inherit = 'account.move'

    @api.constrains('payment_state')
    def payment_show(self):
        for rec in self:
            sale_order_id = rec.mapped('invoice_line_ids.sale_line_ids.order_id')[:1]
            if rec.payment_state == 'paid':
                if sale_order_id.picking_ids:
                    for pick in sale_order_id.picking_ids:
                        if pick.picking_type_code == 'outgoing':
                            pick.show_reg_payment = False



class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    unit_price = fields.Float(related='move_id.sale_line_id.price_unit', string='Unit Price')

class StockMove(models.Model):
    _inherit = 'stock.move.line'

    unit_price = fields.Float(string='Unit Price',related='move_id.sale_line_id.price_unit')
    discount = fields.Float(string='Discount',related='move_id.sale_line_id.discount')
    tax_id = fields.Many2many('account.tax',string='Tax',related='move_id.sale_line_id.tax_id')
    price_subtotal = fields.Monetary(compute='_compute_amount',
                                     string='Subtotal', store=True)
    price_total = fields.Monetary(compute='_compute_amount', string='Total',
                                  store=True)
    currency_id = fields.Many2one('res.currency',compute='_compute_amount')
    price_tax = fields.Float(compute='_compute_amount', string='Total Tax', readonly=True, store=True)
    qty_done_default = fields.Boolean(default=False)
    is_check = fields.Boolean(default=False)

    @api.constrains('location_dest_id')
    def change_location_dest_id(self):
        for rec in self:
            if rec.is_check is False and rec.picking_id.picking_type_id.name == 'Stack':
                rec.is_check = True
                rec.location_dest_id = rec.product_id.putaway_rule_ids.mapped('location_out_id').id

    def return_product(self):
        ctx = dict(
            default_product_id=self.product_id.id,
        )
        return {
            'name': 'Delivery Return',
            'type': 'ir.actions.act_window',
            'res_model': 'delivery.return.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'context': ctx
        }

    @api.depends('qty_done', 'unit_price', 'tax_id',
                 )
    def _compute_amount(self):
        for line in self:
            line.currency_id = line.move_id.sale_line_id.order_id.currency_id
            price = line.unit_price * (1 - (line.discount or 0.0) / 100.0)
            taxes = line.tax_id.compute_all(price,
                                            line.move_id.sale_line_id.order_id.currency_id,
                                            line.qty_done,
                                            product=line.product_id,
                                            partner=line.move_id.sale_line_id.order_id.partner_shipping_id)
            line.update({
                'price_tax': sum(
                    t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })


    @api.constrains('product_uom_qty')
    def _done_qty(self):
        for rec in self:
            if rec.move_id.picking_id.picking_type_code == 'outgoing':
                if not rec.qty_done_default:

                    rec.move_id.quantity_done = rec.move_id.reserved_availability
                    rec.qty_done = rec.product_uom_qty
                    rec.qty_done_default = True


class StockMoveInherit(models.Model):
    _inherit = 'stock.move'

    reason = fields.Char()











