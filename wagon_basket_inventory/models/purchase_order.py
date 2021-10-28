from odoo import models, fields, api,_
from odoo.exceptions import AccessError, UserError, ValidationError



class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    vendor_id = fields.Many2one('res.partner', string='Suggested Vendor')

    def _prepare_invoice(self):
        """Prepare the dict of values to create the new invoice for a purchase order.
        """
        self.ensure_one()
        move_type = self._context.get('default_move_type', 'in_invoice')
        journal = self.env['account.move'].with_context(
            default_move_type=move_type)._get_default_journal()
        if not journal:
            raise UserError(
                _('Please define an accounting purchase journal for the company %s (%s).') % (
                self.company_id.name, self.company_id.id))

        partner_invoice_id = self.partner_id.address_get(['invoice'])['invoice']
        invoice_vals = {
            'ref': self.partner_ref or '',
            'move_type': move_type,
            'narration': self.notes,
            'currency_id': self.currency_id.id,
            'invoice_user_id': self.user_id and self.user_id.id,
            'partner_id': partner_invoice_id,
            'fiscal_position_id': (
                        self.fiscal_position_id or self.fiscal_position_id.get_fiscal_position(
                    partner_invoice_id)).id,
            'payment_reference': self.partner_ref or '',
            'vendor_id':self.vendor_id,
            'partner_bank_id': self.partner_id.bank_ids[:1].id,
            'invoice_origin': self.name,
            'invoice_payment_term_id': self.payment_term_id.id,
            'invoice_line_ids': [],
            'company_id': self.company_id.id,
        }
        return invoice_vals


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    barcode = fields.Char(string='Barcode')
    mrp = fields.Float('MRP')
    available_qty = fields.Char(string="Onhand Qty",compute='_compute_available_qty',store=True)

    @api.depends('product_id')
    def _compute_available_qty(self):
        for rec in self:
            if rec.product_id:
                rec.available_qty = rec.product_id.qty_available

    @api.onchange('barcode')
    def _onchange_barcode(self):
        if self.barcode:
            product = self.env['product.product'].search(
                [('barcode', '=', self.barcode)])
            if product:
                self.product_id = product.id

    @api.onchange('product_id')
    def _onchange_product(self):
        if self.product_id:
            product = self.env['product.product'].search(
                [('id', '=', self.product_id.id)])
            if product:
                self.barcode = product.barcode


class AccountMove(models.Model):
    _inherit = 'account.move'

    vendor_id = fields.Many2one('res.partner', string='Suggested Vendor',)

class PurchaseRequisitionLine(models.Model):
    _inherit = 'purchase.requisition.line'

    barcode = fields.Char(string="Barcode")

    @api.onchange('barcode')
    def _onchange_barcode(self):
        if self.barcode:
            product = self.env['product.product'].search(
                [('barcode', '=', self.barcode)])
            if product:
                self.product_id = product.id

    @api.onchange('product_id')
    def _onchange_product(self):
        if self.product_id:
            product = self.env['product.product'].search(
                [('id', '=', self.product_id.id)])
            if product:
                self.barcode = product.barcode







