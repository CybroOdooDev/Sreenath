from odoo import fields, models, api, _
import json
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta



class BarcodeActionQualityCheck(models.TransientModel):
    _inherit = "barcodes.barcode_events_mixin"
    _name = "quantity.segregation"
    _description = "Segregation"

    model = fields.Char(required=True, readonly=True, default='quantity.segregation')
    method = fields.Char(required=True, readonly=True, default='find_package_by_ref_using_barcode')
    name = fields.Char('Name', default='Segregation', readonly=True)
    scanned_package_ids = fields.One2many('stock.quant.package', compute='_compute_scanned_package_idss')
    last_scanned_order = fields.Many2one('sale.order', string="Last Scanned Sale Order",
                                         related='last_scanned_pack.sale_id')
    last_scanned_slot = fields.Selection([
        ('s1', 'S1'),
        ('s2', 'S2'),
        ('s3', 'S3'),
        ('s4', 'S4')
    ], string='Last Scanned Slot', related='last_scanned_pack.slot', store=True
    )
    last_scanned_route = fields.Many2one('route.mapping', string="Route(Last Scanned)",
                                         related='last_scanned_order.route_id')
    last_scanned_pack = fields.Many2one('stock.quant.package', string="Last Scanned Package",
                                        compute='_compute_scanned_package_idss')
    shift_one_crates = fields.One2many('stock.quant.package', compute='_compute_scanned_package_idss')
    shift_two_crates = fields.One2many('stock.quant.package', compute='_compute_scanned_package_idss')

    @api.depends('name')
    def _compute_scanned_package_idss(self):
        crate = self.env['stock.quant.package'].search([('last_scanned', '=', True)], limit=1)
        self.last_scanned_pack = crate.id
        packs = []
        for each in self.env['stock.quant.package'].search([]):
            if each.sale_id and each.sub_id and each.status == 'scanned' and each.picking_id.state == 'done' :
                if each.id not in packs:
                    packs.append(each.id)
        for rec in self:
            rec.scanned_package_ids = packs
            rec.shift_one_crates = rec.scanned_package_ids.filtered(lambda s: s.sale_id.shift == 'shift1' and s.sale_id.deliver_date == fields.Date.today()+ relativedelta(days=1))
            rec.shift_two_crates = rec.scanned_package_ids.filtered(lambda s: s.sale_id.shift == 'shift2' and s.sale_id.deliver_date == fields.Date.today())

    def find_package_by_ref_using_barcode(self, barcode):
        package = self.env['stock.quant.package'].search([('name', '=', barcode)], limit=1)
        if not package:
            raise ValidationError(_(
                "Package with Barcode %s cannot be found"
            )
                                  % barcode)
        package.segregation_status = 'scanned'
        package.last_scanned = True
        pack_search = self.env['stock.quant.package'].search([('last_scanned', '=', True), ('id', '!=', package.id)])
        if pack_search:
            pack_search.last_scanned = False
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }


class StockQuantPackage(models.Model):
    _inherit = 'stock.quant.package'

    segregation_status = fields.Selection([
        ('scanned', 'Scanned'),
        ('not-scanned', 'Not Scanned')], string="Status", default="not-scanned")
    last_scanned = fields.Boolean(default=False, copy=False)
