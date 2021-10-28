from odoo import models, fields, api, _
from odoo.exceptions import UserError


class StockPickingBatchInherit(models.Model):
    _inherit = 'stock.picking.batch'

    sub_id = fields.Many2one("product.subtype", string="Cluster")
    delivery_date = fields.Date(string='Delivery Date', default=fields.Date.today())
    del_time_slot = fields.Selection([
        ('s1', '07:00 - 10:00(S1)'),
        ('s2', '10:00 - 13:00(S2)'),
        ('s3', '15:00 - 18:00(S3)'),
        ('s4', '18:00 - 21:00(S4)')
    ], string='Slot'
    )

    picking_type_id = fields.Many2one(
        'stock.picking.type', 'Operation Type', check_company=True, copy=False,
        readonly=True, required=True, states={'draft': [('readonly', False)]})

    move_ids = fields.One2many(
        'stock.move', string="Stock moves", compute='_compute_move_ids', readonly=False)

    trolley_id = fields.Many2one("inventory.trolley", string="Trolley")

    picking_filter_ids = fields.Many2many('stock.picking', readonly=True)

    picking_ids = fields.One2many(
        'stock.picking', 'batch_id', string='Transfers', readonly=True,
        domain="[('id', 'in', allowed_picking_ids),('id','in',picking_filter_ids)]", check_company=True,
        states={'draft': [('readonly', False)], 'in_progress': [('readonly', False)]},
        help='List of transfers associated to this batch')
    allowed_picking_ids = fields.One2many('stock.picking', compute='_compute_allowed_picking_ids')
    is_pick = fields.Boolean(string="Is Pick", default=False)
    add_product = fields.Boolean(related='picking_type_id.add_product')
    put_in_pack = fields.Boolean(related='picking_type_id.put_in_pack')
    crate_ids = fields.One2many('stock.quant.package', compute='_compute_move_ids')
    employee_id = fields.Many2one('hr.employee', string='Employee Responsible',compute='_compute_employee_id')
    employee_code = fields.Char(string='Employee Code',copy=False)

    @api.depends('employee_code')
    def _compute_employee_id(self):
        for rec in self:
            search_employee = self.env['hr.employee'].search([('identification_id','=',rec.employee_code)],limit=1)
            if search_employee and rec.employee_code:
                rec.employee_id = search_employee.id
            else:
                rec.employee_id = False

    @api.depends('company_id', 'picking_type_id', 'state')
    def _compute_allowed_picking_ids(self):
        allowed_picking_states = ['waiting', 'confirmed', 'assigned']
        cancelled_batchs = self.env['stock.picking.batch'].search_read(
            [('state', '=', 'cancel')], ['id']
        )
        cancelled_batch_ids = [batch['id'] for batch in cancelled_batchs]

        for batch in self:
            domain_states = list(allowed_picking_states)
            # Allows to add draft pickings only if batch is in draft as well.
            if batch.state == 'draft':
                domain_states.append('draft')
            domain = [
                ('company_id', '=', batch.company_id.id),
                ('immediate_transfer', '=', False),
                ('state', 'in', domain_states),
                '|',
                '|',
                ('batch_id', '=', False),
                ('batch_id', '=', batch.id),
                ('batch_id', 'in', cancelled_batch_ids),
            ]
            if batch.picking_type_id:
                domain += [('picking_type_id', '=', batch.picking_type_id.id)]
            batch.allowed_picking_ids = self.env['stock.picking'].search(domain)

        operation_type = self.picking_type_id

        if operation_type.name == 'Pick':
            self.is_pick = True
        else:
            self.is_pick = False

    @api.depends('picking_ids', 'picking_ids.move_line_ids', 'picking_ids.move_lines', 'picking_ids.move_lines.state')
    def _compute_move_ids(self):
        for batch in self:
            batch.move_ids = batch.picking_ids.move_lines
            batch.move_line_ids = batch.picking_ids.move_line_ids
            for line in batch.move_line_ids:
                if line.trolley_location_id:
                    if type(line.id) == int:
                        new_line = self.env['stock.move.line'].search(
                            [('move_id', '=', line.move_id.id), ('id', '!=', line.id)])
                        if new_line:
                            new_line.sudo().write({
                                'trolley_location_id': line.trolley_location_id.id
                            })
            batch.show_check_availability = any(m.state not in ['assigned', 'done'] for m in batch.move_ids)

            if any(line.reserved_availability != 0 for line in self.move_ids):
                self.show_check_availability = False
        for rec in self:
            rec.crate_ids = False
            if rec.state != 'draft':
                for m in rec.move_ids:
                    if m.trolley_location_id:
                        search_pack = self.env['stock.quant.package'].search(
                            [('batch_id', '=', rec.id), ('sale_id', '=', m.picking_id.sale_id.id),
                             ('sub_id', '=', rec.sub_id.id)])
                        search_pack.trolley_location_id = m.trolley_location_id.id
                crates = self.env['stock.quant.package'].search([('batch_id', '=', rec.id)])
                rec.crate_ids = crates.ids

            else:
                rec.crate_ids = False

    @api.onchange('sub_id', 'delivery_date', 'del_time_slot')
    def get_picking_ids(self):
        if self.sub_id and not self.delivery_date and not self.del_time_slot:
            product_ids = self.env['product.product'].search([('sub_ids', '=', self.sub_id.id)])
            if product_ids:
                move_line_ids = self.env['stock.move'].search([('product_id', 'in', product_ids.ids)])
                if move_line_ids:
                    picking_ids = move_line_ids.mapped('picking_id')
                    self.picking_filter_ids = picking_ids
        elif self.delivery_date and not self.sub_id and not self.del_time_slot:
            picking_ids = self.env['stock.picking'].search([('sale_id.deliver_date', '=', self.delivery_date)])
            # picking_ids = self.env['stock.picking'].filtered(lambda l:l.sale_id.deliver_date == self.delivery_date)
            self.picking_filter_ids = picking_ids.ids
        elif self.del_time_slot and not self.sub_id and not self.delivery_date:
            picking_ids = self.env['stock.picking'].search([('sale_id.slot', '=', self.del_time_slot)])
            self.picking_filter_ids = picking_ids.ids
        elif self.delivery_date and self.del_time_slot and not self.sub_id:
            picking_ids = self.env['stock.picking'].search(
                [('sale_id.slot', '=', self.del_time_slot), ('sale_id.deliver_date', '=', self.delivery_date)])

            # picking_ids = self.env['stock.picking'].filtered(lambda l:l.sale_id.deliver_date == self.delivery_date and l.sale_id.slot == self.del_time_slot)
            self.picking_filter_ids = picking_ids.ids
        elif self.sub_id and self.del_time_slot and not self.delivery_date:
            product_ids = self.env['product.product'].search([('sub_ids', '=', self.sub_id.id)])
            if product_ids:
                move_line_ids = self.env['stock.move'].search([('product_id', 'in', product_ids.ids)])
                if move_line_ids:
                    picking_ids = move_line_ids.mapped('picking_id')
                    self.picking_filter_ids = picking_ids
                # if self.delivery_date and self.del_time_slot:
                b = self.picking_filter_ids.filtered(
                    lambda l: l.sale_id.slot == self.del_time_slot)
                if len(b) != 0:

                    self.picking_filter_ids = b.ids
                else:
                    self.picking_filter_ids = False
        elif self.sub_id and self.delivery_date and not self.del_time_slot:
            product_ids = self.env['product.product'].search([('sub_ids', '=', self.sub_id.id)])
            if product_ids:
                move_line_ids = self.env['stock.move'].search([('product_id', 'in', product_ids.ids)])
                if move_line_ids:
                    picking_ids = move_line_ids.mapped('picking_id')
                    self.picking_filter_ids = picking_ids
                # if self.delivery_date and self.del_time_slot:
                b = self.picking_filter_ids.filtered(
                    lambda l: l.sale_id.deliver_date == self.delivery_date)
                if len(b) != 0:

                    self.picking_filter_ids = b.ids
                else:
                    self.picking_filter_ids = False
        elif self.sub_id and self.delivery_date and self.del_time_slot:
            product_ids = self.env['product.product'].search([('sub_ids', '=', self.sub_id.id)])
            if product_ids:
                move_line_ids = self.env['stock.move'].search([('product_id', 'in', product_ids.ids)])
                if move_line_ids:
                    picking_ids = move_line_ids.mapped('picking_id')
                    self.picking_filter_ids = picking_ids
                # if self.delivery_date and self.del_time_slot:
                b = self.picking_filter_ids.filtered(
                    lambda l: l.sale_id.deliver_date == self.delivery_date and l.sale_id.slot == self.del_time_slot)
                if len(b) != 0:

                    self.picking_filter_ids = b.ids
                else:
                    self.picking_filter_ids = False
        else:
            product_ids = self.env['product.product'].search([])
            if product_ids:
                move_line_ids = self.env['stock.move.line'].search([('product_id', 'in', product_ids.ids)])
                if move_line_ids:
                    picking_ids = move_line_ids.mapped('picking_id')
                    self.picking_filter_ids = picking_ids.ids

    def action_confirm(self):
        for picking in self.picking_ids:
            prev_move_ids = picking.batch_id.move_ids
            updt_move_ids = []
            for move in prev_move_ids:
                if self.sub_id:
                    if self.sub_id.id in move.product_id.sub_ids.ids:
                        updt_move_ids.append(move.id)
                        move.move_for_backorder = False


                    else:
                        move.move_for_backorder = True

                elif not self.sub_id:
                    updt_move_ids.append(move.id)

            picking._create_backorder()
            picking.batch_id.move_ids = [(6, 0, updt_move_ids)]

            prev_move_line_ids = picking.batch_id.move_line_ids
            updt_move_line_ids = []
            for move_line in prev_move_line_ids:
                if self.sub_id:
                    if self.sub_id.id in move_line.product_id.sub_ids.ids:
                        updt_move_line_ids.append(move_line.id)
                elif not self.sub_id:
                    updt_move_line_ids.append(move_line.id)
            picking.batch_id.move_line_ids = [(6, 0, updt_move_line_ids)]
        if self.sub_id:
            for rec in self.picking_ids:
                for line in rec.move_line_ids:
                    if self.sub_id.id in line.product_id.sub_ids.ids:
                        pack = self.env['stock.quant.package'].search(
                            [('sale_id', '=', rec.sale_id.id), ('sub_id', '=', self.sub_id.id),
                             ('batch_id', '=', self.id)])
                        for qty in range(int(line.product_uom_qty)):
                            if not pack:
                                val = ({
                                    'sale_id': rec.sale_id.id,
                                    'sub_id': self.sub_id.id,
                                    'move_line_id': line.id,
                                    'batch_id': self.id
                                })
                                pack = self.env['stock.quant.package'].create(val)

                            line.result_package_id = pack.id
                        # if line.result_package_id:
                        #     line.write({
                        #         'result_package_id':False
                        #     })
                        #
                        # line_qty = line.move_id.product_qty
                        # quant = self.env['stock.quant'].search([('location_id','=',line.location_id.id),('product_id','=',line.product_id.id)])
                        # for stock_quant in quant:
                        #     if not stock_quant.package_id:
                        #         inventory_quantity = stock_quant.inventory_quantity
                        #         available_quantity = stock_quant.available_quantity
                        #         stock_quant.sudo().write({
                        #             'inventory_quantity': inventory_quantity-line_qty,
                        #             'available_quantity': available_quantity-line_qty,
                        #             'quantity': stock_quant.quantity-line_qty
                        #         })
                        # new_stock_quant = self.env['stock.quant'].sudo().create({
                        #     'product_id': line.product_id.id,
                        #     'location_id': line.location_id.id,
                        #     'package_id': line.package_id.id,
                        #     'inventory_quantity': line_qty,
                        #     'available_quantity': line_qty,
                        #     'quantity': line_qty
                        # })
                        # pack_level_id = self.env['stock.package_level'].create({
                        #     'package_id': pack.id
                        # })
                        # line.move_id.package_level_id = pack_level_id.id

                # picking._create_backorder()
        res = super(StockPickingBatchInherit, self).action_confirm()
        return res

    def action_done(self):
        res = super(StockPickingBatchInherit, self).action_done()
        self.ensure_one()
        self._check_company()
        pickings = self.mapped('picking_ids').filtered(lambda picking: picking.state not in ('cancel', 'done'))
        if any(picking.state not in ('assigned', 'confirmed') for picking in pickings):
            raise UserError(
                _('Some transfers are still waiting for goods. Please check or force their availability before setting this batch to done.'))

        for picking in pickings:
            picking.message_post(
                body="<b>%s:</b> %s <a href=#id=%s&view_type=form&model=stock.picking.batch>%s</a>" % (
                    _("Transferred by"),
                    _("Batch Transfer"),
                    picking.batch_id.id,
                    picking.batch_id.name))
            for move_line in picking.move_line_ids:
                move_line.qty_done = move_line.product_uom_qty

        if self.sub_id:
            return pickings.with_context(skip_backorder=True,
                                         sub_id=True).button_validate()
        return res

    def get_barcode_view_state(self):
        res = super(StockPickingBatchInherit, self).get_barcode_view_state()
        for batch_picking in res:
            for i in batch_picking['move_line_ids']:
                search_move_line = self.env['stock.move.line'].search(
                    [('id', '=', i['id'])])
                read_move_line = search_move_line.read()
                i['trolley_location_id'] = read_move_line[0]['trolley_location_id']
        return res

    @api.model
    def _get_fields_to_read(self):
        return [
            'company_id',
            'move_line_ids',
            'name',
            'picking_ids',
            'picking_type_id',
            'picking_type_code',
            'state',
            'add_product',
            'put_in_pack'
        ]
