import base64

from odoo import api, models, fields, _
from odoo.tools.safe_eval import safe_eval
from odoo.exceptions import UserError
import requests
import datetime
from bs4 import BeautifulSoup
from odoo.exceptions import ValidationError
import time
from datetime import datetime, timedelta

# Whether you want to pull all the existing integrations from SendCloud.
SENDCLOUD_GET_ALL_EXISTING_INTEGRATIONS = False


class SendCloudIntegration(models.Model):
    _name = "dhl.integration"
    _description = "DHL Integrations"

    client_id = fields.Char(readonly=False)
    client_secret_id = fields.Char(readonly=False)
    sender_address = fields.Many2one('res.partner', readonly=False)
    bearer_token = fields.Char()
    company_id = fields.Many2one(
        "res.company", required=True, default=lambda self: self.env.company)

    street = fields.Char('Street', compute='_compute_partner_address_values', readonly=False, store=True)
    street2 = fields.Char('Street2', compute='_compute_partner_address_values', readonly=False, store=True)
    zip = fields.Char('Zip', change_default=True, compute='_compute_partner_address_values', readonly=False, store=True)
    city = fields.Char('City', compute='_compute_partner_address_values', readonly=False, store=True)
    state_id = fields.Many2one(
        "res.country.state", string='State',
        compute='_compute_partner_address_values', readonly=False, store=True,
        domain="[('country_id', '=?', country_id)]")
    country_id = fields.Many2one(
        'res.country', string='Country',
        compute='_compute_partner_address_values', readonly=False, store=True)

    return_address = fields.Many2one('res.partner', readonly=False)

    return_street = fields.Char('Street', compute='_compute_partner_address_values', readonly=False, store=True)
    return_street2 = fields.Char('Street2', compute='_compute_partner_address_values', readonly=False, store=True)
    return_zip = fields.Char('Zip', change_default=True, compute='_compute_partner_address_values', readonly=False,
                             store=True)
    return_city = fields.Char('City', compute='_compute_partner_address_values', readonly=False, store=True)
    return_state_id = fields.Many2one(
        "res.country.state", string='State',
        compute='_compute_partner_address_values', readonly=False, store=True,
        domain="[('country_id', '=?', country_id)]")
    return_country_id = fields.Many2one(
        'res.country', string='Country',
        compute='_compute_partner_address_values', readonly=False, store=True)

    updated_at = fields.Datetime()
    next_updated_at = fields.Datetime()
    expiry_seconds = fields.Integer()
    customer_identification_no = fields.Char('Customer Identification')

    @api.onchange('sender_address', 'return_address')
    @api.depends('sender_address', 'return_address')
    def _compute_partner_address_values(self):
        for rec in self:
            rec.street = rec.sender_address.street
            rec.street2 = rec.sender_address.street2
            rec.zip = rec.sender_address.zip
            rec.state_id = rec.sender_address.state_id
            rec.city = rec.sender_address.city
            rec.country_id = rec.sender_address.country_id

            rec.return_street = rec.return_address.street
            rec.return_street2 = rec.return_address.street2
            rec.return_zip = rec.return_address.zip
            rec.return_state_id = rec.return_address.state_id
            rec.return_city = rec.return_address.city
            rec.return_country_id = rec.return_address.country_id

    def dhl_credentials(self):
        for rec in self:
            return rec.client_id, rec.client_secret_id, rec.bearer_token

    def get_bearer_token(self):
        for rec in self:
            if rec.client_id and rec.client_secret_id:
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                expiry = now + timedelta(seconds=rec.expiry_seconds)
                expiry_time = expiry.strftime("%H:%M:%S")

                if current_time >= expiry_time:
                    print('innnnnnnnnn')
                    urls = "https://api-sandbox.dhl.com/ccc/v1/auth/accesstoken"
                    response = requests.request("GET", urls, auth=(str(rec.client_id), str(rec.client_secret_id)))
                    tokens = response.json()
                    rec.bearer_token = tokens['access_token']
                    rec.expiry_seconds = tokens['expires_in']


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def load_cpan_payload(self):
        for order in self:
            for rec in order.picking_ids:
                sequence_id = self.env['ir.sequence'].next_by_code('dhl.integration')
                dhl_cred = self.env['dhl.integration'].search([], limit=1)
                if order.partner_id.country_id.intrastat:
                    parcel_product = 'ParcelEurope.parcelconnect'
                else:
                    parcel_product = 'ParcelEurope.parcelinternational'
                if dhl_cred:
                    if dhl_cred.customer_identification_no:
                        if dhl_cred.street:
                            if dhl_cred.street2:
                                if dhl_cred.zip:
                                    if dhl_cred.city:
                                        if dhl_cred.country_id:
                                            payload = {
                                                "dataElement": {
                                                    "parcelOriginOrganization": dhl_cred.sender_address.country_id.code,
                                                    "parcelDestinationOrganization": order.partner_id.country_id.code,
                                                    "general": {
                                                        "parcelIdentifier": sequence_id,
                                                        "timestamp": "2016-11-06T10:30:28Z",
                                                        "product": parcel_product,
                                                        "routingCode": "2LHR10090+70000000"
                                                    },
                                                    "cPAN": {
                                                        "addresses": {
                                                            "sender": {
                                                                "type": "default",
                                                                "firstName": order.company_id.name,
                                                                "name": order.company_id.name,
                                                                "street1": dhl_cred.street,
                                                                "street1Nr": dhl_cred.street2,
                                                                "postcode": dhl_cred.zip,
                                                                "city": dhl_cred.city,
                                                                "country": dhl_cred.sender_address.country_id.code,
                                                                "referenceNr": "REF45678901234567890123456789012345",
                                                                "customerIdentification": dhl_cred.customer_identification_no,
                                                                "customerAccountNr1": "Test5012345678",
                                                                "hs_code": order.order_line[0].product_id.code
                                                            },
                                                            "recipient": {
                                                                "type": "parcelshops",
                                                                "firstName": order.partner_id.name,
                                                                "name": order.partner_id.name,
                                                                "additionalName": order.partner_id.name,
                                                                "mobileNr": order.partner_id.phone,
                                                                "email": order.partner_id.email,
                                                                "street1": order.partner_id.street_name,
                                                                "street1Nr": order.partner_id.street_number,
                                                                "postcode": order.partner_id.zip,
                                                                "city": order.partner_id.city,
                                                                "country": order.partner_id.country_id.code,
                                                                "customerIdentification": "6199546008"
                                                            }
                                                        },
                                                        "features": {
                                                            "physical": {
                                                                "grossWeight": rec.weight
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                            return payload
                                        else:
                                            raise ValidationError(
                                                _("Please check wheather the country is given in the sender address "))
                                    else:
                                        raise ValidationError(
                                            _("Please check wheather the city is given in the sender address "))
                                else:
                                    raise ValidationError(
                                        _("Please check wheather the zip is given in the sender address "))
                            else:
                                raise ValidationError(
                                    _("Please check wheather the street2 is given in the sender address "))
                        else:
                            raise ValidationError(_("Please check wheather the street is given in the sender address "))
                    else:
                        raise ValidationError(
                            _("Please check wheather the Customer Identification No is given in the sender address "))

    def load_return_cpan_payload(self):
        for order in self:
            for rec in order.picking_ids:
                sequence_id = self.env['ir.sequence'].next_by_code('dhl.integration')
                dhl_cred = self.env['dhl.integration'].search([], limit=1)
                if dhl_cred:
                    if dhl_cred.customer_identification_no:
                        if dhl_cred.street:
                            if dhl_cred.street2:
                                if dhl_cred.zip:
                                    if dhl_cred.city:
                                        if dhl_cred.country_id:
                                            payload = {
                                                "dataElement": {
                                                    "parcelOriginOrganization": dhl_cred.sender_address.country_id.code,
                                                    "parcelDestinationOrganization": order.partner_id.country_id.code,
                                                    "general": {
                                                        "parcelIdentifier": sequence_id,
                                                        "timestamp": "2016-11-06T10:30:28Z",
                                                        "product": 'parceleurope.return.network',
                                                        "routingCode": "2LHR10090+70000000"
                                                    },
                                                    "cPAN": {
                                                        "addresses": {
                                                            "sender": {
                                                                "type": "default",
                                                                "firstName": order.company_id.name,
                                                                "name": order.company_id.name,
                                                                "street1": dhl_cred.street,
                                                                "street1Nr": dhl_cred.street2,
                                                                "postcode": dhl_cred.zip,
                                                                "city": dhl_cred.city,
                                                                "country": dhl_cred.sender_address.country_id.code,
                                                                "referenceNr": "REF45678901234567890123456789012345",
                                                                "customerIdentification": dhl_cred.customer_identification_no,
                                                                "customerAccountNr1": "Test5012345678",
                                                                "hs_code": order.order_line[0].product_id.code
                                                            },
                                                            "recipient": {
                                                                "type": "parcelshops",
                                                                "firstName": order.partner_id.name,
                                                                "name": order.partner_id.name,
                                                                "additionalName": order.partner_id.name,
                                                                "mobileNr": order.partner_id.phone,
                                                                "email": order.partner_id.email,
                                                                "street1": order.partner_id.street_name,
                                                                "street1Nr": order.partner_id.street_number,
                                                                "postcode": order.partner_id.zip,
                                                                "city": order.partner_id.city,
                                                                "country": order.partner_id.country_id.code,
                                                                "customerIdentification": "6199546008"
                                                            }
                                                        },
                                                        "features": {
                                                            "physical": {
                                                                "grossWeight": rec.weight
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                            return payload
                                        else:
                                            raise ValidationError(
                                                _("Please check wheather the country is given in the sender address "))
                                    else:
                                        raise ValidationError(
                                            _("Please check wheather the city is given in the sender address "))
                                else:
                                    raise ValidationError(
                                        _("Please check wheather the zip is given in the sender address "))
                            else:
                                raise ValidationError(
                                    _("Please check wheather the street2 is given in the sender address "))
                        else:
                            raise ValidationError(_("Please check wheather the street is given in the sender address "))
                    else:
                        raise ValidationError(
                            _("Please check wheather the Customer Identification No is given in the sender address "))

    def load_ccustom_items(self):
        for order in self:
            items = []
            dhl_cred = self.env['dhl.integration'].search([], limit=1)
            for rec in order.order_line:
                items.append({
                    "description": rec.product_id,
                    "customsTariffNumber": rec.product_id.intrastat_id,
                    "originCountry": rec.product_id.intrastat_origin_country_id.code,
                    "quantity": rec.product_uom_qty,
                    "netWeight": rec.product_id.weight * rec.product_uom_qty,
                    "value": rec.price_subtotal
                })
            return items

    def load_ccustom_payload(self):
        for order in self:
            for rec in order.picking_ids:
                sequence_id = self.env['ir.sequence'].next_by_code('dhl.integration')
                dhl_cred = self.env['dhl.integration'].search([], limit=1)
                invoice_id = order.invoice_ids
                # if invoice_id:
                #     invoices = self.env['account.move'].search([('id', '=', invoice_id)])
                if dhl_cred:
                    if order.partner_id.country_id.intrastat:
                        parcel_product = 'ParcelEurope.parcelconnect'
                    else:
                        parcel_product = 'ParcelEurope.parcelinternational'
                    print('ParcelEurope.parcelconnect', parcel_product)

                    payload = {
                        "dataElement": {
                            "version": "0200",
                            "parcelOriginOrganization": dhl_cred.sender_address.country_id.code,
                            "parcelDestinationOrganization": order.partner_id.country_id.code,
                            "general": {
                                "parcelIdentifier": sequence_id,
                                "timestamp": "2020-05-22T11:15:15",
                                "product": parcel_product,
                                "routingCode": "2LHR10090+70000001",
                                "customerIdentification": dhl_cred.customer_identification_no
                            },

                            "cCustoms": {
                                "CustomsIDs": {
                                    "sender": [
                                        {
                                            "idType": "VAT",
                                            "identifier": dhl_cred.sender_address.vat
                                        },
                                        {
                                            "idType": "EORI",
                                            "identifier": dhl_cred.sender_address.eori_no
                                        }
                                    ],
                                    "recipient": [
                                        {
                                            "idType": "VAT",
                                            "identifier": order.partner_id.vat
                                        },
                                        {
                                            "idType": "EORI",
                                            "identifier": order.partner_id.eori_no
                                        }
                                    ]
                                },
                                "shippingFee": {
                                    "currency": order.currency_id.name,
                                    "value": "5.50"
                                },
                                "goodsDescription": {
                                    "general": {
                                        "goodsClassification": "Other",
                                        "currency": order.currency_id.name,
                                    },
                                    "item": self.load_ccustom_items()
                                },
                                "customsDocuments": {
                                    "document": [
                                        {
                                            "docType": "Invoice",
                                            "identifier": order.name
                                        },
                                        {
                                            "docType": "license",
                                            "identifier": ""
                                        }
                                    ]
                                },
                                "comment": order.note
                            }
                        }
                    }
                    return payload

    def action_parcel_items(self):
        for order in self:
            for rec in order.picking_ids:
                parcel_items = []
                for item in rec.move_ids_without_package:
                    parcel_items.append((0, 0, {
                        "description": item.product_id.name,
                        "quantity": order.order_line[0].product_uom_qty,
                        "weight": rec.weight,
                        "value": order.amount_total,
                        "product_id": item.product_id.id,
                        "parcel_id": item.product_id.id,
                    }))
                    return parcel_items

    def request_wrapper(self, status_code):
        for rec in self:
            urls = "https://api-sandbox.dhl.com/ccc/v1/auth/accesstoken"
            dhl_credentials = self.env['dhl.integration'].search([], limit=1)
            response = requests.request("GET", urls, auth=(
                str(dhl_credentials.client_id), str(dhl_credentials.client_secret_id)))
            if status_code == 401:
                api_response = requests.request("GET", urls, auth=(
                    str(dhl_credentials.client_id), str(dhl_credentials.client_secret_id)))
                api_tokens = response.json()
                if api_response.status_code == 200:
                    dhl_credentials.bearer_token = api_tokens['access_token']
                    return dhl_credentials.bearer_token

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for order in self:
            print('order.partner_id.read()', order.partner_id.read())
            for rec in order.picking_ids:
                if rec != 0:
                    if rec.delivery_type == 'dhl':
                        dhl_credentials = self.env['dhl.integration'].search([], limit=1)

                        bearer_token = dhl_credentials.bearer_token

                        cpan_url = "https://api-sandbox.dhl.com/ccc/send-cpan"
                        ccustom_url = "https://api-sandbox.dhl.com/ccc/send-cCustoms"

                        querystring_pdf = {"generateLabel": "true", "labelFormat": "pdf",
                                           'labelSize': order.carrier_id.label_size}
                        querystring_zpl = {"generateLabel": "true", "labelFormat": "zpl",
                                           'labelSize': order.carrier_id.label_size,
                                           'resolution': order.carrier_id.resolution}

                        headerss = {
                            "content-type": "application/json",
                            "Authorization": "Bearer" + ' ' + bearer_token
                        }

                        cpan_payload = order.load_cpan_payload()
                        print('cccccccccc', cpan_payload['dataElement']['general']['parcelIdentifier'])

                        ccustoms_payload = order.load_ccustom_payload()
                        print('cccccccccc', ccustoms_payload['dataElement']['general']['parcelIdentifier'])


                        cpan_responses_pdf = requests.request("POST", cpan_url, json=cpan_payload, headers=headerss,
                                                              params=querystring_pdf)
                        cpan_responses_zpl = requests.request("POST", cpan_url, json=cpan_payload, headers=headerss,
                                                              params=querystring_zpl)

                        if order.partner_id.country_id.intrastat:
                            parcel_product = 'ParcelEurope.parcelconnect'
                        else:
                            parcel_product = 'ParcelEurope.parcelinternational'
                        print('ParcelEurope.parcelconnect', parcel_product)

                        c_custom_payload = {
                            "dataElement": {
                                "version": "0200",
                                "parcelOriginOrganization": dhl_credentials.sender_address.country_id.code,
                                "parcelDestinationOrganization": order.partner_id.country_id.code,
                                "general": {
                                    "parcelIdentifier": cpan_payload['dataElement']['general']['parcelIdentifier'],
                                    "timestamp": "2020-05-22T11:15:15",
                                    "product": 'ParcelEurope.parcelinternational',
                                    "routingCode": "2LHR10090+70000001",
                                    "customerIdentification": dhl_credentials.customer_identification_no
                                },

                                "cCustoms": {
                                    "CustomsIDs": {
                                        "sender": [
                                            {
                                                "idType": "VAT",
                                                "identifier": dhl_credentials.sender_address.vat
                                            },
                                            {
                                                "idType": "EORI",
                                                "identifier": dhl_credentials.sender_address.eori_no
                                            }
                                        ],
                                        "recipient": [
                                            {
                                                "idType": "VAT",
                                                "identifier": order.partner_id.vat
                                            },
                                            {
                                                "idType": "EORI",
                                                "identifier": order.partner_id.eori_no
                                            }
                                        ]
                                    },
                                    "shippingFee": {
                                        "currency": order.currency_id.name,
                                        "value": "5.50"
                                    },
                                    "goodsDescription": {
                                        "general": {
                                            "goodsClassification": "Other",
                                            "currency": order.currency_id.name,
                                        },
                                        "item": self.load_ccustom_items()
                                    },
                                    "customsDocuments": {
                                        "document": [
                                            {
                                                "docType": "Invoice",
                                                "identifier": order.name
                                            },
                                            {
                                                "docType": "license",
                                                "identifier": "123"
                                            }
                                        ]
                                    },
                                    "comment": order.note
                                }
                            }
                        }

                        ccustom_responses_pdf = requests.request("POST", ccustom_url, json=c_custom_payload, headers=headerss)

                        print('ccustom_responses_pdf', ccustom_responses_pdf)
                        print('status_code', ccustom_responses_pdf.status_code)
                        print('content', ccustom_responses_pdf.content)

                        if cpan_responses_pdf.status_code == 401:
                            bearer_tokens = self.request_wrapper(cpan_responses_pdf.status_code)

                        if cpan_responses_pdf.status_code == 200:
                            print('rrrrrrreeeeeeeeessssssssssspppppp', cpan_responses_pdf.content)
                            dhl_parcel = self.env['dhl.parcel']
                            parcels = {
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
                                'tracking_number': '1',
                                'order_number': rec.sale_id.name,
                                'customs_invoice_nr': rec.sale_id.partner_invoice_id.name,
                                'company_id': self.env.company.id,

                                'picking_id': rec.id,
                                'is_cpan': True,

                                'parcel_item_ids': [(0, 0, {
                                    "description": item.product_id.name,
                                    "quantity": order.order_line[0].product_uom_qty,
                                    "weight": rec.weight,
                                    "volume": rec.volume,
                                    "hs_code": order.order_line[0].product_id.intrastat_id.code,
                                    "value": order.amount_total,
                                    "product_id": item.product_id.id,
                                    "parcel_id": item.product_id.id,
                                }) for item in rec.move_ids_without_package]
                            }

                            sequence_id = self.env['ir.sequence'].next_by_code('dhl.integration')

                            parcel = dhl_parcel.create(parcels)
                            language = self.env['res.lang'].search([('code', '=', order.partner_id.lang)])
                            parcel.tracking_url = "https://www.dhl.com/" + order.partner_id.country_id.code + "-" + language.url_code + "/home/tracking/tracking-global-forwarding.html?submit=1&tracking-id=" + 'JJD14999029999959750'
                            report = self.env['ir.attachment'].sudo().create({
                                'name': sequence_id + '.pdf',
                                'type': 'binary',
                                'datas': base64.encodestring(cpan_responses_pdf.content),
                                'mimetype': 'application/x-pdf',
                                'res_model': 'dhl.parcel',
                                'res_id': parcel.id,
                            })

                            soup = BeautifulSoup(cpan_responses_pdf.text, 'html.parser')
                            links = soup.find_all('a')
                            pick = self.env['stock.picking'].search([('id', '=', order.picking_ids[-1].id)])
                            pick.is_cpan = True
                            pick.dhl_ids = parcel.id
                            pick.dhl_ids.cpan_pdf = report.ids
                            import PyPDF2

                            pdfFileObj = open('/home/cybrosys/PycharmProjects/odoo14/odoo/fruvi_dev/dhl_connectors/static/description/CPAN0000000003-3.pdf', 'rb')
                            pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
                            print(pdfReader.numPages)
                            pageObj = pdfReader.getPage(0)
                            print('***************************************', pageObj.extractText())
                            pdfFileObj.close()

                        if cpan_responses_zpl.status_code == 200:
                            reports = self.env['ir.attachment'].sudo().create({
                                'name': sequence_id + '.zpl',
                                'type': 'binary',
                                'datas': base64.encodestring(cpan_responses_zpl.content),
                                'mimetype': '',
                            })
                            pick.dhl_ids.cpan_zpl = reports.ids

                        return res


class ResCompany(models.Model):
    _inherit = 'res.company'

    eori_no = fields.Char('EORI Number')


class ResPartner(models.Model):
    _inherit = 'res.partner'

    eori_no = fields.Char('EORI Number')
