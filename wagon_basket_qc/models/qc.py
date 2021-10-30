from odoo import fields, models, api, _
import json
from odoo.exceptions import ValidationError

from odoo.tools.safe_eval import safe_eval


class BarcodeActionQualityCheck(models.TransientModel):
    _name = "quantity.check"
    _inherit = "barcodes.barcode_events_mixin"
    _description = "Quantity Check"

    model = fields.Char(required=True, readonly=True, default='quantity.check')
    res_id = fields.Integer()
    method = fields.Char(required=True, readonly=True, default='find_package_by_ref_using_barcode')
    state = fields.Selection(
        [("waiting", "Waiting"), ("warning", "Warning")],
        default="waiting",
        readonly=True,
    )
    status = fields.Text(readonly=True, default="Start scanning")
    name = fields.Char(string='Name', default='Quantity Check', readonly=True)
    quantity_check_package_ids = fields.One2many('stock.quant.package', compute='_compute_quality_check_package_ids',
                                                 order='status')
    total_crates = fields.Integer(string='Total Crates', compute='_compute_crate_count')
    scanned_crates = fields.Integer(string='Scanned Crates', compute='_compute_crate_count')
    not_scanned_crates = fields.Integer(string='Not Scanned Crates', compute='_compute_crate_count')

    @api.depends('name')
    def _compute_quality_check_package_ids(self):
        operation_type = self.env['stock.picking.type'].search([('name', '=', 'QC')])
        pickings = self.env['stock.picking'].search(
            [('picking_type_id', '=', operation_type.id), ('state', '=', 'assigned')])
        packs = []
        for pick in pickings:
            for line in pick.move_line_ids:
                if line.package_id:
                    if not line.package_id.id in packs:
                        line.package_id.picking_id = pick.id
                        packs.append(line.package_id.id)
        for each in self.env['stock.quant.package'].search([]):
            if each.sale_id and each.sub_id and each.extra_created and (each.status=='not-scanned' or not each.sale_id.sudo().is_pack_validated) :
                if each.id not in packs:
                    packs.append(each.id)
        for rec in self:
            rec.quantity_check_package_ids = packs

    def find_package_by_ref_using_barcode(self, barcode):
        package = self.env['stock.quant.package'].search([('name', '=', barcode)], limit=1)
        if not package:
            raise ValidationError(_(
                "Package with Barcode %s cannot be found"
            )
                                  % barcode)

        package.status = 'scanned'
        pack_search = self.env['stock.quant.package'].search([('last_scanned','=',True),('id','!=',package.id)])
        if pack_search:
            pack_search.last_scanned = False
        operation_type = self.env['stock.picking.type'].search([('name', '=', 'QC')])
        pickings = self.env['stock.picking'].search(
            [('picking_type_id', '=', operation_type.id), ('state', '=', 'assigned')])
        for pick in pickings:
            packs = []
            for line in pick.move_line_ids:
                if line.package_id:
                    if not line.package_id.id in packs:
                        packs.append(line.package_id.id)
            packages = self.env['stock.quant.package'].search(
                [('status', '=', 'scanned'), ('picking_id', '=', pick.id)]).ids
            if sorted(packs) == sorted(packages):
                for move_line in pick.move_line_ids:
                    move_line.move_id.quantity_done = move_line.move_id.reserved_availability
                    move_line.qty_done = move_line.product_uom_qty
                pick.with_context(skip_backorder=True).sudo().button_validate()
            if pick.state == 'done':
                pick.sale_id.sudo().is_pack_validated = True

        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

    @api.depends('quantity_check_package_ids')
    def _compute_crate_count(self):
        for rec in self:
            package_ids = []
            for sale in rec.quantity_check_package_ids:
                sales = self.env['sale.order'].search([('id', '=', sale.sale_id.id)])
                package = self.env['stock.quant.package'].search([('id', '=', sale.sale_id.id)], limit=1)
                if package.sale_id.shift:
                    package_ids.append(package.id)
            rec.total_crates = len(package_ids)
            rec.scanned_crates = len(rec.quantity_check_package_ids.filtered(lambda l: l.status == 'scanned'))
            rec.not_scanned_crates = len(rec.quantity_check_package_ids.filtered(lambda l: l.status == 'not-scanned'))




class StockQuantPackage(models.Model):
    _inherit = 'stock.quant.package'

    status = fields.Selection([
        ('scanned', 'Scanned'),
        ('not-scanned', 'Not Scanned')], string="Status", default="not-scanned")
    product_count = fields.Integer(compute='_compute_product_count')
    route_id = fields.Many2one(related='sale_id.route_id')
    slot = fields.Selection([
        ('s1', 'S1'),
        ('s2', 'S2'),
        ('s3', 'S3'),
        ('s4', 'S4')
    ], string='Slot', related='sale_id.slot', store=True
    )


    @api.depends('quant_ids.product_id')
    def _compute_product_count(self):
        for rec in self:
            rec.product_count =0
            for line in rec.quant_ids:
                rec.product_count += line.quantity


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    is_pack_validated = fields.Boolean(default=False,copy=False)

