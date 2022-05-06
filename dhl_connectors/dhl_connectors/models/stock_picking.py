
# Copyright 2021 Onestein (<https://www.onestein.nl>)
# License OPL-1 (https://www.odoo.com/documentation/14.0/legal/licenses.html#odoo-apps).
import base64
from collections import defaultdict
import logging
import json
import uuid

import requests
from bs4 import BeautifulSoup

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.safe_eval import safe_eval
from odoo import api, models, fields, _
from odoo.tools.safe_eval import safe_eval
from odoo.exceptions import UserError
import requests
import datetime
from bs4 import BeautifulSoup
from odoo.exceptions import ValidationError
import time
from datetime import datetime, timedelta

_logger = logging.getLogger(__name__)


class StockPicking(models.Model):
    _inherit = "stock.picking"

    dhl_ids = fields.Many2one("dhl.parcel")
    return_dhl_ids = fields.Many2one("dhl.return.parcel")
    dhl_parcel_count = fields.Integer(string="Parcels", compute="_compute_dhl_parcel_count")
    dhl_return_parcel_count = fields.Integer(string="Return Parcels", compute="_compute_dhl_return_parcel_count")
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
            current_picking_move_line_ids = self.env['stock.move.line'].search([('picking_id', '=', rec.id)])
            volume = rec.product_id.mapped('volume')
            if volume:
                rec.volume = volume[0]
            else:
                rec.volume = 0

    @api.depends("dhl_ids")
    def _compute_dhl_parcel_count(self):
        for picking in self:
            picking.dhl_parcel_count = len(picking.dhl_ids)

    @api.depends("return_dhl_ids")
    def _compute_dhl_return_parcel_count(self):
        for picking in self:
            picking.dhl_return_parcel_count = len(picking.return_dhl_ids)

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

    def action_open_dhl_parcels_return(self):
        self.ensure_one()
        if len(self.return_dhl_ids) == 1:
            return {
                "type": "ir.actions.act_window",
                "res_model": "dhl.return.parcel",
                "res_id": self.return_dhl_ids.id,
                "view_mode": "form",
                "context": self.env.context,
            }
        return {
            "type": "ir.actions.act_window",
            "name": _("DHL Parcels"),
            "res_model": "dhl.return.parcel",
            "domain": [("id", "in", self.return_dhl_ids.id)],
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

                return parcel


class ReturnPicking(models.TransientModel):
    _inherit = 'stock.return.picking'

    def _create_returns(self):
        new_picking_idss = super(ReturnPicking, self)._create_returns()
        picking_id = self.env['stock.picking'].search(
            [('id', '=', new_picking_idss), ('picking_type_code', '=', 'incoming')])
        dhl_return_parcel = self.env['dhl.return.parcel']
        for rec in picking_id:
            for order in self.picking_id.sale_id:
                cpan_url = "https://api-sandbox.dhl.com/ccc/send-cpan"
                ccustom_url = "https://api-sandbox.dhl.com/ccc/send-cpan?generateLabel=true&labelFormat=pdf"

                dhl_credentials = self.env['dhl.integration'].search([], limit=1)

                querystring_pdf = {"generateLabel": "true", "labelFormat": "pdf",
                                   'labelSize': order.carrier_id.label_size}
                querystring_zpl = {"generateLabel": "true", "labelFormat": "zpl",
                                   'labelSize': order.carrier_id.label_size, 'resolution': order.carrier_id.resolution}

                if dhl_credentials.client_id and dhl_credentials.client_secret_id:
                    now = datetime.now()
                    current_time = now.strftime("%H:%M:%S")
                    expiry = now + timedelta(seconds=0)
                    expiry_time = expiry.strftime("%H:%M:%S")

                    if current_time == expiry_time:
                        urls = "https://api-sandbox.dhl.com/ccc/v1/auth/accesstoken"
                        response = requests.request("GET", urls,
                                                    auth=(str(dhl_credentials.client_id),
                                                          str(dhl_credentials.client_secret_id)))
                        tokens = response.json()
                        dhl_credentials.bearer_token = tokens['access_token']
                        dhl_credentials.write({'bearer_token': tokens['access_token']})

                bearer_token = tokens['access_token']
                headerss = {
                    "content-type": "application/json",
                    "Authorization": "Bearer" + ' ' + bearer_token
                }
                if order.partner_id.country_id.intrastat == True:
                    cpan_payload = order.load_return_cpan_payload()
                    ccustoms_payload = order.load_cpan_payload()

                    cpan_responses_pdf = requests.request("POST", cpan_url, json=cpan_payload, headers=headerss,
                                                          params=querystring_pdf)
                    cpan_responses_zpl = requests.request("POST", cpan_url, json=cpan_payload, headers=headerss,
                                                          params=querystring_zpl)

                    ccustoms_responses = requests.request("POST", ccustom_url, json=ccustoms_payload,
                                                          headers=headerss)
                    parcels = {
                        'sender_partner_name': rec.partner_id.name,
                        'sender_address': rec.partner_id.street,
                        'sender_house_number': rec.partner_id.street_number,

                        'sender_street': rec.partner_id.street_name,
                        'sender_city': rec.partner_id.city,
                        'sender_postal_code': rec.partner_id.zip,
                        'sender_country_iso_2': rec.partner_id.country_id.name,
                        'sender_email': rec.partner_id.email,
                        'sender_telephone': rec.partner_id.mobile,

                        'partner_name': dhl_credentials.return_address.name,
                        'address': dhl_credentials.return_address.street,
                        'house_number': dhl_credentials.return_address.street_number,

                        'street': dhl_credentials.return_address.street_name,
                        'city': dhl_credentials.return_address.city,
                        'postal_code': dhl_credentials.return_address.zip,
                        'country_iso_2': dhl_credentials.return_address.country_id.name,
                        'email': dhl_credentials.return_address.email,
                        'telephone': dhl_credentials.return_address.mobile,
                        'company_name': picking_id.partner_id.commercial_company_name,
                        'name': picking_id.name,
                        'tracking_number':  cpan_responses_pdf.headers['shipmentId'],
                        'order_number': rec.sale_id.name,
                        'customs_invoice_nr': rec.sale_id.partner_invoice_id.name,
                        'company_id': self.env.company.id,

                        'picking_id': picking_id.id,
                        'is_cpan': True,
                        'is_return': True,
                        'return_delivery_duties': rec.sale_id.carrier_id.return_delivery_duties,

                        'return_parcel_item_ids': [(0, 0, {
                            "return_description": item.product_id.name,
                            "return_quantity": item.product_uom_qty,
                            "return_weight": picking_id.weight,
                            "return_volume": picking_id.volume,
                            "return_hs_code": item.product_id.intrastat_id.code,
                            "return_value": order.amount_total,
                            "return_product_id": item.product_id.id,
                            "return_parcel_id": item.product_id.id,
                        }) for item in rec.move_ids_without_package]
                    }

                    sequence_id = self.env['ir.sequence'].next_by_code('dhl.integration.return')

                    parcel = dhl_return_parcel.create(parcels)
                    language = self.env['res.lang'].search([('code', '=', order.partner_id.lang)])
                    parcel.tracking_url = "https://www.dhl.com/" + order.partner_id.country_id.code + "-" + language.url_code + "/home/tracking/tracking-global-forwarding.html?submit=1&tracking-id=" + \
                                          cpan_responses_pdf.headers['shipmentId']

                    pick = self.env['stock.picking'].search([('id', '=', order.picking_ids[-1].id)])
                    if cpan_responses_pdf.status_code == 200:
                        report = self.env['ir.attachment'].sudo().create({
                            'name': sequence_id + '.pdf',
                            'type': 'binary',
                            'datas': base64.encodestring(cpan_responses_pdf.content),
                            'mimetype': 'application/x-pdf',
                            'res_model': 'dhl.return.parcel',
                            'res_id': parcel.id,
                        })

                        soup = BeautifulSoup(cpan_responses_pdf.text, 'html.parser')
                        links = soup.find_all('a')

                        pick.is_cpan = True
                        pick.return_dhl_ids = parcel.id
                        pick.return_dhl_ids.cpan_pdf = report.ids

                    if cpan_responses_zpl.status_code == 200:
                        reports = self.env['ir.attachment'].sudo().create({
                            'name': sequence_id + '.zpl',
                            'datas': base64.encodestring(cpan_responses_zpl.content),
                            'mimetype': '',
                        })
                        pick.return_dhl_ids = parcel.id

                        pick.return_dhl_ids.cpan_zpl = reports.ids
                # raise ValidationError(_('Return shipment from outside the European Union are currently not supported by DHL Parcel Connect'))

                return new_picking_idss
