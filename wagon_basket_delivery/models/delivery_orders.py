from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare, float_is_zero, float_round


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    show_reg_payment = fields.Boolean(default=False)
    employee_id = fields.Many2one('hr.employee', string='Employee')
    employee_code = fields.Char(string='Employee Code')
    package_count = fields.Integer(string='Package', compute='_compute_package_count')
    route_id = fields.Many2one('route.mapping')
    deliver_date = fields.Date(related='sale_id.deliver_date', store=True)
    delivery_return_id = fields.Many2one('stock.picking')
    is_delivery_return = fields.Boolean(compute='compute_is_delivery_return')

    def compute_is_delivery_return(self):
        picking_type_id = self.env.ref(
            'wagon_basket_delivery.delivery_return_operation_type')

        for rec in self:
            if rec.picking_type_id.id == picking_type_id.id:
                rec.is_delivery_return = True
            else:
                rec.is_delivery_return = False

    @api.onchange('employee_code')
    def _onchange_employee_code(self):
        if self.employee_code:
            employee = self.env['hr.employee'].search([('identification_id','=',self.employee_code)])
            self.employee_id = employee.id if employee else False

    def _compute_package_count(self):
        for rec in self:
            packages = rec.move_line_ids.mapped('package_id')
            package_count = self.env['stock.quant.package'].search_count([('id','in', packages.ids)])
            rec.package_count = package_count

    def button_validate(self):
        print("button_validate")
        # Clean-up the context key at validation to avoid forcing the creation of immediate
        # transfers.
        ctx = dict(self.env.context)
        ctx.pop('default_immediate_transfer', None)
        self = self.with_context(ctx)

        # Sanity checks.
        pickings_without_moves = self.browse()
        pickings_without_quantities = self.browse()
        pickings_without_lots = self.browse()
        products_without_lots = self.env['product.product']
        for picking in self:
            if not picking.move_lines and not picking.move_line_ids:
                pickings_without_moves |= picking

            picking.message_subscribe([self.env.user.partner_id.id])
            picking_type = picking.picking_type_id
            precision_digits = self.env['decimal.precision'].precision_get('Product Unit of Measure')
            no_quantities_done = all(float_is_zero(move_line.qty_done, precision_digits=precision_digits) for move_line in picking.move_line_ids.filtered(lambda m: m.state not in ('done', 'cancel')))
            no_reserved_quantities = all(float_is_zero(move_line.product_qty, precision_rounding=move_line.product_uom_id.rounding) for move_line in picking.move_line_ids)
            if no_reserved_quantities and no_quantities_done:
                pickings_without_quantities |= picking

            if picking_type.use_create_lots or picking_type.use_existing_lots:
                lines_to_check = picking.move_line_ids
                if not no_quantities_done:
                    lines_to_check = lines_to_check.filtered(lambda line: float_compare(line.qty_done, 0, precision_rounding=line.product_uom_id.rounding))
                for line in lines_to_check:
                    product = line.product_id
                    if product and product.tracking != 'none':
                        if not line.lot_name and not line.lot_id:
                            pickings_without_lots |= picking
                            products_without_lots |= product

        if not self._should_show_transfers():
            if pickings_without_moves:
                raise UserError(_('Please add some items to move.'))
            if pickings_without_quantities:
                raise UserError(self._get_without_quantities_error_message())
            if pickings_without_lots:
                raise UserError(_('You need to supply a Lot/Serial number for products %s.') % ', '.join(products_without_lots.mapped('display_name')))
        else:
            message = ""
            if pickings_without_moves:
                message += _('Transfers %s: Please add some items to move.') % ', '.join(pickings_without_moves.mapped('name'))
            if pickings_without_quantities:
                message += _('\n\nTransfers %s: You cannot validate these transfers if no quantities are reserved nor done. To force these transfers, switch in edit more and encode the done quantities.') % ', '.join(pickings_without_quantities.mapped('name'))
            if pickings_without_lots:
                message += _('\n\nTransfers %s: You need to supply a Lot/Serial number for products %s.') % (', '.join(pickings_without_lots.mapped('name')), ', '.join(products_without_lots.mapped('display_name')))
            if message:
                raise UserError(message.lstrip())

        # Run the pre-validation wizards. Processing a pre-validation wizard should work on the
        # moves and/or the context and never call `_action_done`.
        if not self.env.context.get('button_validate_picking_ids'):
            self = self.with_context(button_validate_picking_ids=self.ids)
        res = self._pre_action_done_hook()
        if res is not True:
            return res

        # Call `_action_done`.
        if self.env.context.get('picking_ids_not_to_backorder'):
            pickings_not_to_backorder = self.browse(self.env.context['picking_ids_not_to_backorder'])
            print("pickings_not_to_backorder",pickings_not_to_backorder)
            pickings_to_backorder = self - pickings_not_to_backorder
            print('pickings_to_backorder',pickings_to_backorder)
        else:
            pickings_not_to_backorder = self.env['stock.picking']
            print("else",pickings_not_to_backorder)
            pickings_to_backorder = self
            print("else",pickings_to_backorder)
        pickings_not_to_backorder.sudo().with_context(cancel_backorder=True)._action_done()
        pickings_to_backorder.sudo().with_context(cancel_backorder=False)._action_done()
        for rec in self:
            if rec.picking_type_code == 'outgoing':
                rec.sale_id.sudo()._create_invoices()
                for invoice in rec.sale_id.invoice_ids:
                    invoice.sudo().action_post()
                    rec.show_reg_payment = True

        return True

    def button_validate_2(self):
        self.with_context(skip_backorder=True,
                          picking_ids_not_to_backorder=self.id).button_validate()


    def action_payment(self):
        invoice_ids = self.sale_id.invoice_ids
        # search = self.env['account.move'].search([('id','=',invoice_ids[0])])

        return {
            'name': _('Register Payment'),
            'res_model': 'account.payment.register',
            'view_mode': 'form',
            'context': {
                'active_model': 'account.move',
                'active_ids': invoice_ids.ids,
            },
            'target': 'new',
            'type': 'ir.actions.act_window',
        }

    # @api.depends('sale_id')
    # def _compute_employee_id











