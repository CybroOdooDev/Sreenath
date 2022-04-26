import base64

from odoo import api, models, fields, _
from odoo.tools.safe_eval import safe_eval
from odoo.exceptions import UserError
import requests
import datetime
from bs4 import BeautifulSoup

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

    @api.onchange('sender_address')
    @api.depends('sender_address')
    def _compute_partner_address_values(self):
        for rec in self:
            rec.street = rec.sender_address.street
            rec.street2 = rec.sender_address.street2
            rec.zip = rec.sender_address.zip
            rec.state_id = rec.sender_address.state_id
            rec.city = rec.sender_address.city
            rec.country_id = rec.sender_address.country_id


    def dhl_credentials(self):
        for rec in self:
            return rec.client_id, rec.client_secret_id, rec.bearer_token

    def get_bearer_token(self):
        for rec in self:
            if rec.client_id and rec.client_secret_id:
                uurl = "https://api-sandbox.dhl.com"
                urls = "https://api-sandbox.dhl.com/ccc/v1/auth/accesstoken"
                response = requests.request("GET", urls, auth=(str(rec.client_id), str(rec.client_secret_id)))
                tokens = response.json()
                rec.bearer_token = tokens['access_token']

                querystring = {"generateLabel": "true", "labelFormat": "pdf"}

                ct = datetime.datetime.now()

                url = "https://api-sandbox.dhl.com/ccc/send-cpan?generateLabel=true&labelFormat=pdf"

                sequence_id = self.env['ir.sequence'].next_by_code('dhl.integration')

                print('ssssssss', sequence_id)
                payload = {
                    "dataElement": {
                        "parcelOriginOrganization": "AT",
                        "parcelDestinationOrganization": "DE",
                        "general": {
                            "parcelIdentifier": sequence_id,
                            # "timestamp": datetime.datetime.now(),
                            "product": "ParcelEurope.parcelconnect",
                            "routingCode": "2LHR10090+70000000"
                        },
                        "cPAN": {
                            "addresses": {
                                "sender": {
                                    "type": "default",
                                    "firstName": "Good Weather GmbH",
                                    "name": "c/o DHL Parcel Europe",
                                    "street1": "Robert-Bosch-Str.",
                                    "street1Nr": "750",
                                    "postcode": "93055",
                                    "city": "Regensburg",
                                    "country": "DE",
                                    "referenceNr": "REF45678901234567890123456789012345",
                                    "customerIdentification": "6199546008",
                                    "customerAccountNr1": "Test5012345678"
                                },
                                "recipient": {
                                    "type": "parcelshop",
                                    "firstName": "John",
                                    "name": "Doe",
                                    "additionalName": "Rain Inc.",
                                    "mobileNr": "+491234567890",
                                    "email": "john.doe@example.com",
                                    "street1": "DHL Paketshop",
                                    "street1Nr": "414",
                                    "postcode": "53111",
                                    "city": "Bonn",
                                    "country": "DE",
                                    "customerIdentification": ""
                                }
                            },
                            "features": {
                                "physical": {
                                    "grossWeight": "1.0"
                                }
                            }
                        }
                    }
                }

                headerss = {
                    "content-type": "application/json",
                    "Authorization": "Bearer" + ' ' + tokens['access_token']
                }
                print('headerss', headerss)

                responsess = requests.request("POST", url,
                                              json=payload, headers=headerss)

                with open('Catssssssssss.pdf', 'wb') as f:
                    f.write(response.content)

                report = self.env['ir.attachment'].sudo().create({
                    'name': '!!!!!!!!!!!!!!!!!!!!!!!',
                    'type': 'binary',
                    'datas': base64.encodestring(responsess.content),
                    # 'res_model': 'dhl.parcel',
                    'mimetype': 'application/x-pdf'
                })
                print('report', report)
                print('report', report.read())
                print('**********************', responsess.content)

                soup = BeautifulSoup(responsess.text, 'html.parser')
                links = soup.find_all('a')
                print('soup', soup)
                print('links', links)

                # # if present download file
                # for link in links:
                #     if ('.pdf' in link.get('href', [])):
                #         i += 1
                #         print("Downloading file: ", i)
                #         # Get response object for link
                # r_response = requests.get(link.get('href'))
                # Write content in pdf file

                send_customs_url = uurl + '/ccc/send-cCustoms'
                print('semnd_customs', send_customs_url)

                send_customs_headers = {
                    "content-type": "application/json",
                    "Authorization": "Bearer" + ' ' + tokens['access_token']
                }

                send_custom_payload = {"dataElement": {
                    "version": "0201",
                    "parcelOriginOrganization": "DE",
                    "parcelDestinationOrganization": "JP",
                    "general": {
                        "parcelIdentifier": "CPAN202111513460",
                        "timestamp": "2016-11-06T10:30:28Z",
                        "product": "ParcelEurope.parcelinternational",
                        "routingCode": "2LDE00017",
                        "customerIdentification": "6199546008"
                    },
                    "cCustoms": {
                        "CustomsIDs": {
                            "sender": [
                                {
                                    "idType": "VAT",
                                    "identifier": "789012"
                                },
                                {
                                    "idType": "EORI",
                                    "identifier": "123"
                                }
                            ],
                            "recipient": [
                                {
                                    "idType": "VAT",
                                    "identifier": "789012"
                                },
                                {
                                    "idType": "EORI",
                                    "identifier": "12345"
                                }
                            ]
                        },
                        "shippingFee": {
                            "currency": "EUR",
                            "value": "5.50"
                        },
                        "goodsDescription": {
                            "general": {
                                "goodsClassification": "Other",
                                "currency": "EUR"
                            },
                            "item": [
                                {
                                    "description": "Teedose",
                                    "customsTariffNumber": "234567",
                                    "originCountry": "DE",
                                    "quantity": "2",
                                    "netWeight": "0.100",
                                    "value": "4.00"
                                },
                                {
                                    "description": "Jasmintee",
                                    "customsTariffNumber": "123456",
                                    "originCountry": "DE",
                                    "quantity": "5",
                                    "netWeight": "0.250",
                                    "value": "16.00"
                                }
                            ]
                        },
                        "customsDocuments": {
                            "document": [
                                {
                                    "docType": "Invoice",
                                    "identifier": "20200405_12345"
                                },
                                {
                                    "docType": "license",
                                    "identifier": "999999999999"
                                }
                            ]
                        },
                        "comment": "Test Comment"
                    }
                }
                }

                send_customs_querystring = {"shipmentId": "1"}

                send_customs_responsess = requests.request("POST", url, params=send_customs_querystring,
                                                           json=send_custom_payload, headers=send_customs_headers)

                print('send_customs_responsess', send_customs_responsess.text)
                return report


class SaleOrder(models.Model):
    _inherit = 'sale.order'

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

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for order in self:
            for rec in order.picking_ids:
                if rec != 0:
                    if rec.delivery_type == 'dhl':
                        uurl = "https://api-sandbox.dhl.com"
                        urls = "https://api-sandbox.dhl.com/ccc/v1/auth/accesstoken"

                        dhl_cred = self.env['dhl.integration'].search([], limit=1)

                        response = requests.request("GET", urls,
                                                    auth=(str(dhl_cred.client_id), str(dhl_cred.client_secret_id)))

                        tokens = response.json()
                        bearer_token = dhl_cred.bearer_token

                        querystring = {"generateLabel": "true", "labelFormat": "pdf"}

                        url = "https://api-sandbox.dhl.com/ccc/send-cpan?generateLabel=true&labelFormat=pdf"

                        sequence_id = self.env['ir.sequence'].next_by_code('dhl.integration')
                        payload = {
                            "dataElement": {
                                "parcelOriginOrganization": "AT",
                                "parcelDestinationOrganization": "GB",
                                "general": {
                                    "parcelIdentifier": sequence_id,
                                    "timestamp": "2016-11-06T10:30:28Z",
                                    "product": "ParcelEurope.parcelconnect",
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
                                            "country": dhl_cred.country_id.code,
                                            "referenceNr": "REF45678901234567890123456789012345",
                                            "customerIdentification": "6199546008",
                                            "customerAccountNr1": "Test5012345678",
                                            "hs_code": "Test5012345678"
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
                                            "country": "GB",
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
                        headerss = {
                            "content-type": "application/json",
                            "Authorization": "Bearer" + ' ' + tokens['access_token']
                        }

                        print('payloadpayload', payload)

                        cpan_responses = requests.request("POST", url, json=payload, headers=headerss)

                        print('cpan_responses', cpan_responses)
                        print('textttttttttttt', cpan_responses.text)
                        # if rec.delivery_type == 'dhl':

                        with open('CPAN.pdf', 'wb') as f:
                            f.write(response.content)

                        report = self.env['ir.attachment'].sudo().create({
                            'name': sequence_id + '.pdf',
                            'type': 'binary',
                            'datas': base64.encodestring(cpan_responses.content),
                            # 'res_model': 'dhl.parcel',
                            'mimetype': 'application/x-pdf'
                        })

                        soup = BeautifulSoup(cpan_responses.text, 'html.parser')
                        links = soup.find_all('a')
                        print('reportsssssssss', report)
                        print('soup', soup)

                        dhl_parcel = self.env['dhl.parcel']
                        parcel = dhl_parcel.create({
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
                            'label': report,
                            'tracking_number': '1',
                            'order_number': rec.sale_id.name,
                            'customs_invoice_nr': rec.sale_id.partner_invoice_id.name,
                            'company_id': self.env.company.id,

                            'picking_id': rec.id,

                            'parcel_item_ids': [(0, 0, {
                                "description": item.product_id.name,
                                "quantity": order.order_line[0].product_uom_qty,
                                "weight": rec.weight,
                                "value": order.amount_total,
                                "product_id": item.product_id.id,
                                "parcel_id": item.product_id.id,
                            }) for item in rec.move_ids_without_package]

                        })
                        # parcel.picking_id.dhl_ids = parcel.id

                        return parcel, res
