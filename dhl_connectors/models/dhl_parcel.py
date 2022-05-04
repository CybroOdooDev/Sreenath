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
        'dhl_parcel_id', 'attachment_id', string='Attachments')

    cpan_zpl = fields.Many2many('ir.attachment', 'cpan_zpl_ir_attachments_rel',
        'dhl_parcel_id', 'attachment_id', string='Attachments')

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
            rec.tracking_url = "https://www.dhl.com/"+at-de+"/home/tracking/tracking-global-forwarding.html?submit=1&tracking-id=" + 'JJD14999029999959750'

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

    @api.model
    def _prepare_sendcloud_parcel_from_response(self, parcel):
        res = {
            "name": parcel.get("id"),
            # "sendcloud_code": parcel.get("id"),
            "carrier": parcel.get("carrier", {}).get("code") or parcel.get("carrier"),
        }
        return res

    def action_get_parcel_label(self):
        self.ensure_one()
        if not self.label_printer_url:
            raise UserError(_("Label not available: no label printer url provided."))
        self._generate_parcel_labels()

    def _generate_parcel_labels(self):
        for parcel in self.filtered(lambda p: p.label_printer_url):
            integration = parcel.company_id.sendcloud_default_integration_id
            label = integration.get_parcel_label(parcel.label_printer_url)
            filename = parcel._generate_parcel_label_filename()
            attachment_id = self.env["ir.attachment"].create({
                "name": filename,
                "res_id": parcel.id,
                "res_model": parcel._name,
                "datas": base64.b64encode(label),
                "description": parcel.name,
            })
            parcel.attachment_id = attachment_id

    def _generate_parcel_label_filename(self):
        self.ensure_one()
        if not self.name.lower().endswith('.pdf'):
            return self.name + ".pdf"
        return self.name

    def action_get_return_portal_url(self):
        for parcel in self:
            code = parcel.sendcloud_code
            integration = parcel.company_id.sendcloud_default_integration_id
            response = integration.get_return_portal_url(code)
            if response.get("url") == None:
                parcel.return_portal_url = "None"
            else:
                parcel.return_portal_url = response.get("url")

    @api.model
    def sendcloud_create_update_parcels(self, parcels_data, company_id):

        # All records
        all_records = self.search([("company_id", "=", company_id)])

        # Existing records
        existing_records = all_records.filtered(
            lambda c: c.sendcloud_code in [record["id"] for record in parcels_data]
        )

        # Existing records map (internal code -> existing record)
        existing_records_map = {}
        for existing in existing_records:
            if existing.sendcloud_code not in existing_records_map:
                existing_records_map[existing.sendcloud_code] = self.env[
                    "sendcloud.parcel"
                ]
            existing_records_map[existing.sendcloud_code] |= existing

        # Created records
        vals_list = []
        for record in parcels_data:
            vals = self._prepare_sendcloud_parcel_from_response(record)
            vals["company_id"] = company_id
            if record["id"] in existing_records_map:
                existing_records_map[record["id"]].write(vals)
            else:
                vals_list += [vals]
        new_records = self.create(vals_list)
        new_records.action_get_return_portal_url()

        return existing_records + new_records

    @api.model
    def sendcloud_sync_parcels(self):
        for company in self.env["res.company"].search([]):
            integration = company.sendcloud_default_integration_id
            if integration:
                parcels = integration.get_parcels()
                self.sendcloud_create_update_parcels(parcels, company.id)

    def button_sync_parcel(self):
        self.ensure_one()
        integration = self.company_id.sendcloud_default_integration_id
        if integration:
            parcel = integration.get_parcel(self.sendcloud_code)
            parcels_vals = self.env[
                "sendcloud.parcel"
            ]._prepare_sendcloud_parcel_from_response(parcel)
            self.write(parcels_vals)



    def unlink(self):
        if not self.env.context.get("skip_cancel_parcel"):
            for parcel in self:
                integration = parcel.company_id.sendcloud_default_integration_id
                if integration:
                    res = integration.cancel_parcel(parcel.sendcloud_code)
                    if res.get("error"):
                        if res["error"]["code"] == 404:
                            continue  # ignore "Not Found" error
                        raise UserError(_("SendCloud: %s") % res["error"].get("message"))
        return super().unlink()

    def action_create_return_parcel(self):
        self.ensure_one()
        [action] = self.env.ref(
            "delivery_sendcloud_official.action_sendcloud_create_return_parcel_wizard"
        ).read()
        action["context"] = "{'default_brand_id': %s, 'default_parcel_id': %s}" % (
            self.brand_id.id,
            self.id,
        )
        return action

    @api.model
    def _prepare_sendcloud_parcel_item_from_response(self, data):
        return {
            "description": data.get("description"),
            "quantity": data.get("quantity"),
            "weight": data.get("weight"),
            "value": data.get("value"),
            "hs_code": data.get("hs_code"),
            "origin_country": data.get("origin_country"),
            "product_id": data.get("product_id"),
            "properties": data.get("properties"),
            "sku": data.get("sku"),
            "return_reason": data.get("return_reason"),
            "return_message": data.get("return_message"),
        }



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
    sender_address_2 = fields.Char(help="An apartment or floor number.")
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
                                'dhl_parcel_id', 'attachment_id', string='CPAN PDF')

    cpan_zpl = fields.Many2many('ir.attachment', 'return_cpan_zpl_ir_attachments_rel',
                                'dhl_parcel_id', 'attachment_id', string='CPAN ZPL')

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
            rec.tracking_url = "https://www.dhl.com/"+at-de+"/home/tracking/tracking-global-forwarding.html?submit=1&tracking-id=" + 'JJD14999029999959750'
