# Copyright 2021 Onestein (<https://www.onestein.nl>)
# License OPL-1 (https://www.odoo.com/documentation/14.0/legal/licenses.html#odoo-apps).

from collections import defaultdict
import logging
import json
import uuid

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.safe_eval import safe_eval

_logger = logging.getLogger(__name__)


class StockPicking(models.Model):
    _inherit = "stock.picking"

    dhl_ids = fields.Many2one("dhl.parcel", "picking_id")
    dhl_parcel_count = fields.Integer(string="Parcels", compute="_compute_dhl_parcel_count")
    is_cpan = fields.Boolean('CPAN Parcel', store=True)
    volume = fields.Char(compute='_compute_volume', help="Total volume of all the products contained in the package.")

    def button_validate(self):
        res = super(StockPicking, self).button_validate()
        for rec in self:
            if rec.is_cpan == False:
                raise ValidationError(_("Please create CPAN before validating the picking"))

        return res

    def _compute_volume(self):
        for rec in self:
            print('recccc', rec.read())
            current_picking_move_line_ids = self.env['stock.move.line'].search([('picking_id', '=', rec.id)])
            volume = rec.product_id.mapped('volume')
            if volume:
                rec.volume = volume[0]
            else:
                rec.volume = 0

    #                 for ml in current_picking_move_line_ids:
    #                     weight += ml.product_uom_id._compute_quantity(
    #                         ml.qty_done, ml.product_id.uom_id) * ml.product_id.weight
    #             else:
    #                 for quant in package.quant_ids:
    #                     weight += quant.quantity * quant.product_id.weight
    #             package.weight = weight

    @api.depends("dhl_ids")
    def _compute_dhl_parcel_count(self):
        for picking in self:
            picking.dhl_parcel_count = len(picking.dhl_ids)

    def action_open_dhl_parcels(self):
        self.ensure_one()
        if len(self.dhl_ids) == 1:
            return {
                "type": "ir.actions.act_window",
                "res_model": "dhl.parcel",
                "res_id": self.dhl_ids.id,
                "view_mode": "form",
                "context": self.env.context,
            }
        return {
            "type": "ir.actions.act_window",
            "name": _("DHL Parcels"),
            "res_model": "dhl.parcel",
            "domain": [("id", "in", self.dhl_ids.ids)],
            "view_mode": "tree,form",
            "context": self.env.context,
        }

    def button_create_sendcloud_labels(self):
        for rec in self:
            if rec.delivery_type == 'dhl':
                parcel = self.env['dhl.parcel'].create({
                    'partner_name': rec.sale_id.partner_shipping_id.name,
                    'address': rec.sale_id.partner_shipping_id.street,
                    'house_number': rec.sale_id.partner_shipping_id.street_number,

                    'street': rec.sale_id.partner_shipping_id.street_name,
                    'city': rec.sale_id.partner_shipping_id.city,
                    'postal_code': rec.sale_id.partner_shipping_id.zip,
                    'country_iso_2': rec.sale_id.partner_shipping_id.country_id.name,
                    'email': rec.sale_id.partner_shipping_id.email,
                    'telephone': rec.sale_id.partner_shipping_id.mobile,
                    'company_name': rec.sale_id.partner_shipping_id.commercial_company_name,

                    'name': rec.name,
                    'label': fields.Binary(related="attachment_id.datas"),
                    'tracking_number': '1',
                    'order_number': rec.sale_id.name,
                    'customs_invoice_nr': rec.sale_id.partner_invoice_id.name,
                    'company_id': self.env.company.id,

                    'picking_id': rec.id,
                })
                print(parcel)

                return parcel
