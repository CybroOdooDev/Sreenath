# Copyright 2021 Onestein (<https://www.onestein.nl>)
# License OPL-1 (https://www.odoo.com/documentation/14.0/legal/licenses.html#odoo-apps).

import json

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.tools import float_round
from odoo.tools.safe_eval import safe_eval


class DeliveryCarrier(models.Model):
    _inherit = "delivery.carrier"

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
        help="When this value is null, the price is calculated based on the pricelist by countries"
    )
    sendcloud_is_return = fields.Boolean()
