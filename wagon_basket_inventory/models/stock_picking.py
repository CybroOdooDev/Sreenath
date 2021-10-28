from odoo import SUPERUSER_ID, _, api, fields, models
from odoo.exceptions import UserError



class StockPickingInherit(models.Model):
    _inherit = 'stock.picking'


    def _default_count(self):
        for rec in self:
            search = self.env['stock.quant.package'].search([('sale_id','=',rec.sale_id.id),('batch_id','=',rec.batch_id.id),('sub_id','=',rec.batch_id.sub_id.id)])
            rec.package_count_for_pick = len(search)

    backorder_check = fields.Boolean('Backorder Check',default=False)
    add_product = fields.Boolean(related='picking_type_id.add_product')
    put_in_pack = fields.Boolean(related='picking_type_id.put_in_pack')
    package_count_for_pick = fields.Integer("Packages",compute=_default_count)

    def action_assign(self):
        """ Check availability of picking moves.
        This has the effect of changing the state and reserve quants on available moves, and may
        also impact the state of the picking as it is computed based on move's states.
        @return: True
        """

        self.filtered(lambda picking: picking.state == 'draft').action_confirm()
        if self.batch_id and self.batch_id.sub_id:

            if self.backorder_id:
                moves = self.mapped('move_lines').filtered(
                    lambda move: move.state not in (
                        'draft', 'cancel', 'done') and move.picking_id.backorder_check == True)
                if not moves:
                    moves = self.mapped('move_lines').filtered(
                        lambda move: move.state not in ('draft', 'cancel',
                                                        'done') and move.picking_id.batch_id.sub_id.id in move.product_id.sub_ids.ids)

            else:
                moves = self.mapped('move_lines').filtered(
                    lambda move: move.state not in ('draft', 'cancel', 'done') and move.picking_id.batch_id.sub_id.id in move.product_id.sub_ids.ids)
        else:

            moves = self.mapped('move_lines').filtered(lambda move: move.state not in ('draft', 'cancel', 'done'))
        if not moves:
            raise UserError(_('Nothing to check the availability for.'))
        # If a package level is done when confirmed its location can be different than where it will be reserved.
        # So we remove the move lines created when confirmed to set quantity done to the new reserved ones.
        package_level_done = self.mapped('package_level_ids').filtered(
            lambda pl: pl.is_done and pl.state == 'confirmed')
        package_level_done.write({'is_done': False})
        prev_ids = self.move_line_ids
        moves._action_assign()
        package_level_done.write({'is_done': True})

        return True


    def action_confirm(self):
        res = super(StockPickingInherit, self).action_confirm()
        self._check_company()
        trolley = self.env['stock.picking.batch'].search([])
        x = self.mapped('package_level_ids').filtered(
            lambda pl: pl.state == 'draft' and not pl.move_ids)
        self.mapped('package_level_ids').filtered(lambda pl: pl.state == 'draft' and not pl.move_ids)._generate_moves()
        # call `_action_confirm` on every draft move
        # if self.env.context['params'].get('model') == 'stock.picking.batch':
        if self.batch_id :
            location_length = 0
            if trolley.trolley_id:
                location_length = len(trolley.trolley_id[0].location_ids)
            existing_picking = ''
            if self.move_lines:
                existing_picking = self.move_lines[0].picking_id
            if trolley.trolley_id:
                location_count = 0
                for picking in self:
                    for rec in picking.move_lines:
                        if location_count < location_length and rec.picking_id == existing_picking:
                            rec.trolley_location_id = trolley.trolley_id[0].location_ids[location_count].id
                            existing_picking = rec.picking_id
                        elif location_count < location_length and rec.picking_id != existing_picking:
                            location_count += 1
                            if location_count < location_length:
                                rec.trolley_location_id = trolley.trolley_id[0].location_ids[location_count].id
                                existing_picking = rec.picking_id
                    for rec in picking.move_line_ids:
                        if location_count < location_length and rec.picking_id == existing_picking:
                            rec.trolley_location_id = trolley.trolley_id[0].location_ids[location_count].id
                            existing_picking = rec.picking_id
                        elif location_count < location_length and rec.picking_id != existing_picking:
                            location_count += 1
                            if location_count < location_length:
                                rec.trolley_location_id = trolley.trolley_id[0].location_ids[location_count].id
                                existing_picking = rec.picking_id

        self.mapped('move_lines') \
            .filtered(lambda move: move.state == 'draft') \
            ._action_confirm()


        self.mapped('move_lines').filtered(
            lambda move: move.state not in ('draft', 'cancel', 'done'))._trigger_scheduler()

        return res

    def _create_backorder(self):
        """ This method is called when the user chose to create a backorder. It will create a new
        picking, the backorder, and move the stock.moves that are not `done` or `cancel` into it.
        """
        backorders = self.env['stock.picking']
        for picking in self:
            if picking.batch_id and picking.batch_id.sub_id:
                moves_to_backorder = picking.move_lines.filtered(lambda x: x.state not in ('done', 'cancel') and x.move_for_backorder == True)
            else:
                moves_to_backorder = picking.move_lines.filtered(lambda x: x.state not in ('done', 'cancel'))
            if moves_to_backorder:
                backorder_picking = picking.copy({
                    'name': '/',
                    'move_lines': [],
                    'move_line_ids': [],
                    'backorder_id': picking.id
                })
                picking.message_post(
                    body=_('The backorder <a href=# data-oe-model=stock.picking data-oe-id=%d>%s</a> has been created.') % (
                        backorder_picking.id, backorder_picking.name))
                moves_to_backorder.write({'picking_id': backorder_picking.id})
                moves_to_backorder.mapped('package_level_id').write({'picking_id':backorder_picking.id})
                moves_to_backorder.mapped('move_line_ids').write({'picking_id': backorder_picking.id})
                backorders |= backorder_picking
                back_order = backorders.search(
                    [('backorder_id.batch_id.sub_id', '!=', False),('backorder_id','=',picking.id)])
                for rec in backorders:
                    if rec.picking_type_code == 'internal':
                        if back_order:
                            for order in back_order:
                                order.backorder_check = True
                            back_order.action_assign()
                            for order in back_order:
                                order.backorder_check = False

        return backorders

    def _get_picking_fields_to_read(self):
        """ List of fields on the stock.picking object that are needed by the
        client action. The purpose of this function is to be overriden in order
        to inject new fields to the client action.
        """
        return [
            'move_line_ids',
            'picking_type_id',
            'location_id',
            'location_dest_id',
            'name',
            'state',
            'picking_type_code',
            'company_id',
            'immediate_transfer',
            'add_product',
            'put_in_pack'
        ]

    def create_package(self):
        self.env['stock.quant.package'].create({
            'sale_id':self.sale_id.id,
            'sub_id':self.batch_id.sub_id.id,
            'batch_id':self.batch_id.id,
            'extra_created':True
        })
        self.package_count_for_pick = self.package_count+1






