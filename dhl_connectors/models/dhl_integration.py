from odoo import api, models, fields, _
from odoo.tools.safe_eval import safe_eval
from odoo.exceptions import UserError
import requests

# Whether you want to pull all the existing integrations from SendCloud.
SENDCLOUD_GET_ALL_EXISTING_INTEGRATIONS = False


class SendCloudIntegration(models.Model):
    _name = "dhl.integration"
    _description = "DHL Integrations"

    client_id = fields.Char(readonly=False)
    client_secret_id = fields.Char(readonly=False)
    bearer_token = fields.Char(compute='get_bearer_token')
    company_id = fields.Many2one(
        "res.company", required=True, default=lambda self: self.env.company
    )

    def get_bearer_token(self):
        for rec in self:
            if rec.client_id and rec.client_secret_id:
                urls = "https://api-sandbox.dhl.com/ccc/v1/auth/accesstoken"
                response = requests.request("GET", urls, auth=(str(rec.client_id), str(rec.client_secret_id)))
                tokens = response.json()
                rec.bearer_token = tokens['access_token']

                url = "https://api-sit.dhl.com/ccc/send-cpan"

                querystring = {"generateLabel": "true", "labelFormat": "pdf"}

                payload = {
                    "dataElement": {
                        "parcelOriginOrganization": "AT",
                        "parcelDestinationOrganization": "DE",
                        "general": {
                            "parcelIdentifier": "CPAN202111513460",
                            "timestamp": "2020-05-22T11:15:15",
                            "product": "ParcelEurope.parcelconnect",
                            "routingCode": "2LHR10090+70000000",
                            "customerIdentification": "6199546008"

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
                                    "customerIdentification": "5012345678",
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
                    "Authorization": "Bearer xGTGkyGdcc0nkR3kXUFyQiPuhmov"
                }

                responsess = requests.request("POST", url, auth=(str(rec.client_id), str(rec.client_secret_id)),
                                              json=payload, headers=headerss, params=querystring)

                print('**********************', responsess.text)
