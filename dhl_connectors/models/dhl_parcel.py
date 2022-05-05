# Copyright 2021 Onestein (<https://www.onestein.nl>)
# License OPL-1 (https://www.odoo.com/documentation/14.0/legal/licenses.html#odoo-apps).

import base64

from odoo import api, models, fields, _
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval


class DHLParcel(models.Model):
    _name = "dhl.parcel"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "DHL Parcel"

    is_cpan = fields.Boolean('CPAN Parcel', store=True)
    partner_name = fields.Char()
    address = fields.Char()
    address_2 = fields.Char(help="An apartment or floor number.")
    house_number = fields.Char()
    street = fields.Char()
    city = fields.Char()
    postal_code = fields.Char()
    company_name = fields.Char()
    country_iso_2 = fields.Char()
    email = fields.Char()
    telephone = fields.Char()
    name = fields.Char(required=True)
    cpan_pdf = fields.Many2many('ir.attachment', 'cpan_pdf_ir_attachments_rel',
                                'dhl_parcel_id', 'attachment_id', string='Attachments', store=True)

    cpan_zpl = fields.Many2many('ir.attachment', 'cpan_zpl_ir_attachments_rel',
                                'dhl_parcel_id', 'attachment_id', string='Attachments', store=True)

    # cpan_zpl = fields.Many2one('ir.attachment', string="Attachment", required=True)
    tracking_url = fields.Char(compute='_compute_tracking_url')
    tracking_number = fields.Char()
    external_reference = fields.Char(
        help="A field to use as a reference for your order."
    )
    weight = fields.Float(help="Weight unit of measure is KG.")
    is_return = fields.Boolean(readonly=True)

    parcel_item_ids = fields.One2many("dhl.parcel.item", "parcel_id")

    note = fields.Text()
    type = fields.Char(
        help="Returns either ‘parcel’ or ‘letter’ by which you can determine the type of your shipment."
    )
    order_number = fields.Char()
    customs_invoice_nr = fields.Char()
    shipment = fields.Char(string="Cached Shipment")
    shipment_id = fields.Many2one("delivery.carrier", compute="_compute_shipment_id")
    reference = fields.Char()

    picking_id = fields.Many2one("stock.picking")
    package_id = fields.Many2one("stock.quant.package")
    carrier = fields.Char()
    company_id = fields.Many2one(
        "res.company",
        required=True,
        compute="_compute_company_id",
        store=True,
        readonly=False,
    )
    brand_id = fields.Many2one(
        "sendcloud.brand", compute="_compute_brand_id", store=True, readonly=False
    )
    attachment_id = fields.Many2one(
        comodel_name="ir.attachment",
        ondelete="cascade",
    )

    def _compute_tracking_url(self):
        for rec in self:
            country_code = rec.picking_id.partner_id.country_id.code
            language = self.env['res.lang'].search([('code', '=', rec.picking_id.partner_id.lang)])
            rec.tracking_url = "https://www.dhl.com/" + country_code + "-" + language.url_code + "/home/tracking/tracking-global-forwarding.html?submit=1&tracking-id=" + 'JJD14999029999959750'

    @api.depends("shipment")
    def _compute_shipment_id(self):
        for parcel in self:
            shipment_data = safe_eval(parcel.shipment or "{}")
            shipment_code = shipment_data.get("id")
            domain = parcel._get_shipment_domain_by_code(shipment_code)
            parcel.shipment_id = self.env["delivery.carrier"].search(domain, limit=1)

    def _get_shipment_domain_by_code(self, shipment_code):
        self.ensure_one()
        return [
            ("company_id", "=", self.company_id.id),
            # ("sendcloud_code", "=", shipment_code),
        ]

    @api.depends("picking_id.company_id")
    def _compute_company_id(self):
        for parcel in self:
            parcel.company_id = parcel.picking_id.company_id or parcel.company_id

    @api.depends("company_id")
    def _compute_brand_id(self):
        for parcel in self:
            brands = parcel.company_id.sendcloud_brand_ids
            # TODO only brands with domain?
            parcel.brand_id = fields.first(brands)

    def button_sync_parcel(self):
        self.ensure_one()
        integration = self.company_id.sendcloud_default_integration_id
        if integration:
            parcel = integration.get_parcel(self.sendcloud_code)
            parcels_vals = self.env["sendcloud.parcel"]._prepare_sendcloud_parcel_from_response(parcel)
            self.write(parcels_vals)


class ReturnParcel(models.Model):
    _name = "dhl.return.parcel"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    is_cpan = fields.Boolean('CPAN Parcel', store=True)
    partner_name = fields.Char()
    address = fields.Char()
    address_2 = fields.Char(help="An apartment or floor number.")
    house_number = fields.Char()
    street = fields.Char()
    city = fields.Char()
    postal_code = fields.Char()
    company_name = fields.Char()
    country_iso_2 = fields.Char()
    email = fields.Char()
    telephone = fields.Char()

    sender_partner_name = fields.Char()
    sender_address = fields.Char()
    sender_address_2 = fields.Char()
    sender_house_number = fields.Char()
    sender_street = fields.Char()
    sender_city = fields.Char()
    sender_postal_code = fields.Char()
    sender_company_name = fields.Char()
    sender_country_iso_2 = fields.Char()
    sender_email = fields.Char()
    sender_telephone = fields.Char()

    name = fields.Char(required=True)

    cpan_pdf = fields.Many2many('ir.attachment', 'return_cpan_pdf_ir_attachments_rel',
                                'dhl_parcel_id', 'attachment_id', string='CPAN PDF', store=True)

    cpan_zpl = fields.Many2many('ir.attachment', 'return_cpan_zpl_ir_attachments_rel',
                                'dhl_parcel_id', 'attachment_id', string='CPAN ZPL', store=True)

    tracking_url = fields.Char(compute='_compute_tracking_url')
    tracking_number = fields.Char()
    external_reference = fields.Char(
        help="A field to use as a reference for your order."
    )
    weight = fields.Float(help="Weight unit of measure is KG.")
    is_return = fields.Boolean(readonly=True)

    note = fields.Text()
    type = fields.Char(
        help="Returns either ‘parcel’ or ‘letter’ by which you can determine the type of your shipment."
    )
    order_number = fields.Char()
    customs_invoice_nr = fields.Char()
    shipment = fields.Char(string="Cached Shipment")
    shipment_id = fields.Many2one("delivery.carrier")
    reference = fields.Char()

    picking_id = fields.Many2one("stock.picking")
    package_id = fields.Many2one("stock.quant.package")
    carrier = fields.Char()
    company_id = fields.Many2one(
        "res.company",
        required=True,
        compute="_compute_company_id",
        store=True,
        readonly=False,
    )
    brand_id = fields.Many2one(
        "sendcloud.brand", compute="_compute_brand_id", store=True, readonly=False
    )
    attachment_id = fields.Many2one(
        comodel_name="ir.attachment",
        ondelete="cascade",
    )
    return_parcel_item_ids = fields.One2many("dhl.return.parcel.item", "return_parcel_id")

    return_delivery_duties = fields.Selection(string='Return Delivery Duties',
                                              selection=[
                                                  ('ddu', 'DDU'),
                                                  ('ddp', 'DDP'),
                                              ])

    def button_sync_return_parcel(self):
        self.ensure_one()
        integration = self.company_id.sendcloud_default_integration_id
        if integration:
            parcel = integration.get_parcel(self.sendcloud_code)
            parcels_vals = self.env[
                "sendcloud.parcel"
            ]._prepare_sendcloud_parcel_from_response(parcel)
            self.write(parcels_vals)


    def _compute_tracking_url(self):
        for rec in self:
            country_code = rec.picking_id.partner_id.country_id.code
            language = self.env['res.lang'].search([('code', '=', rec.picking_id.partner_id.lang)])
            rec.tracking_url = "https://www.dhl.com/" + country_code + "-" + language.url_code + "/home/tracking/tracking-global-forwarding.html?submit=1&tracking-id=" + 'JJD14999029999959750'
