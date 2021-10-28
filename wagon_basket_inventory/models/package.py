from odoo import models, fields, api, _


class StockQuantPackage(models.Model):
    _inherit = 'stock.quant.package'
    picking_id = fields.Many2one('stock.picking')
    extra_created = fields.Boolean(default=False)


    @api.model
    def create(self, vals):
        if ('sale_id' in vals and vals['sale_id']) and (
                'sub_id' in vals and vals['sub_id']):
            if 'sequence_id' not in vals or not vals['sequence_id']:
                sale = self.env['sale.order'].browse(
                    vals['sale_id'])
                cluster = self.env['product.subtype'].browse(vals['sub_id'])
                sequence_id = self.env['ir.sequence'].sudo().search([('name',
                                                                      '=',
                                                                      sale.name + ' ' + _(
                                                                          'Sequence') + ' ' + cluster.subtype),
                                                                     ('prefix',
                                                                      '=',
                                                                      sale.name + '-' + cluster.subtype + '-'),
                                                                     ('padding',
                                                                      '=', 3)])
                if sequence_id:
                    vals['sequence_id'] = sequence_id.id
                if not sequence_id:
                    vals['sequence_id'] = self.env['ir.sequence'].sudo().create(
                        {
                            'name': sale.name + ' ' + _(
                                'Sequence') + ' ' + cluster.subtype,
                            'prefix': sale.name + '-' + cluster.subtype + '-',
                            'padding': 3,
                        }).id
                seq = self.env['ir.sequence'].browse(vals['sequence_id'])
                vals['name'] = seq.next_by_id()
        else:
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'stock.quant.package') or _('Unknown Pack')

        picking_type = super(StockQuantPackage, self).create(vals)

        return picking_type

    sale_id = fields.Many2one('sale.order', string='Sale Order')
    sub_id = fields.Many2one('product.subtype', string='Cluster')
    sequence_id = fields.Many2one(
        'ir.sequence', 'Reference Sequence',
        check_company=True, copy=False)
    move_line_id = fields.Many2one('stock.move.line')
    created_from_batch = fields.Boolean(default=False)
    batch_id = fields.Many2one('stock.picking.batch')

    name = fields.Char(
        'Package Reference', copy=False, index=True, )
    trolley_location_id = fields.Many2one('trolley.location',copy=False)


class StockPickingBatch(models.Model):
    _inherit = 'stock.picking.batch'


    def action_cancel(self):
        res = super(StockPickingBatch, self).action_cancel()
        for rec in self.move_line_ids:
            if rec.package_id:
                quant = self.env['stock.quant'].search(
                    [('location_id', '=', rec.location_id.id),
                     ('product_id', '=', rec.product_id.id),('package_id','=',rec.package_id.id)])
                for q in quant:
                    quant_qty = q.quantity

                    q.sudo().write({
                        'quantity':  0
                    })
                loc_without_package = self.env['stock.quant'].search([('location_id','=',rec.location_id.id),
                                                                      ('product_id','=',rec.product_id.id),('package_id','=',False)])
                loc_qty = loc_without_package.quantity
                loc_without_package.sudo().write({
                    'quantity':quant_qty+loc_qty
                })
        return res

