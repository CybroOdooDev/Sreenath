# Copyright 2021 Onestein (<https://www.onestein.nl>)
# License OPL-1 (https://www.odoo.com/documentation/14.0/legal/licenses.html#odoo-apps).

import json

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.tools import float_round
from odoo.tools.safe_eval import safe_eval


class DeliveryCarrier(models.Model):
    _inherit = "delivery.carrier"

    dhl_country_ids = fields.One2many('dhl.shipping.method.country', 'delivery_carriers', string="Price per Country")

    delivery_type = fields.Selection(
        selection_add=[("dhl", "DHL")],
        ondelete={'dhl': lambda recs: recs.write({
            'delivery_type': 'fixed', 'fixed_price': 0,
        })})

    dhl_code = fields.Integer()
    dhl_carrier = fields.Char()
    dhl_service_point_input = fields.Selection(
        [("none", "None"), ("required", "Required")], default="none"
    )
    dhl_min_weight = fields.Float()
    dhl_max_weight = fields.Float()
    dhl_price = fields.Float(
        help="When this value is null, the price is calculated based on the pricelist by countries")
    sendcloud_is_return = fields.Boolean()
    parcel_origin = fields.Many2one('res.country', string='Parcel Origin', )
    parcel_destination = fields.Many2one('res.country', string='Parcel Destination')
    return_delivery_duties = fields.Selection(string='Return Delivery Duties',
                                              selection=[
                                                  ('ddu', 'DDU'),
                                                  ('ddp', 'DDP'),
                                              ], default='ddu')

    label_size = fields.Selection(string='Label SIze',
                                  selection=[
                                      ('10x15', '10x15'),
                                      ('10x21', '10x21'),
                                  ])

    resolution = fields.Selection(string='Resolution',
                                  selection=[
                                      ('200', '200'),
                                      ('300', '300'),
                                  ])


class ChooseDeliveryCarrier(models.TransientModel):
    _inherit = 'choose.delivery.carrier'

    def _get_shipment_rate(self):
        vals = self.carrier_id.rate_shipment(self.order_id)
        if vals:
            if vals.get('success'):
                self.delivery_message = vals.get('warning_message', False)
                self.delivery_price = vals['price']
                self.display_price = vals['carrier_price']
                return {}
        else:
            if self.carrier_id.delivery_type == 'dhl':
                self.delivery_price = float(self.carrier_id.dhl_price) * (1.0 + (self.carrier_id.margin / 100.0))
                self.display_price = self.delivery_price
            else:
                return {'error_message': vals['error_message']}
            return {}
