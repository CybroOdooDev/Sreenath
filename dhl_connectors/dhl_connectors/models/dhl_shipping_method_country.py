# Copyright 2021 Onestein (<https://www.onestein.nl>)
# License OPL-1 (https://www.odoo.com/documentation/14.0/legal/licenses.html#odoo-apps).

from odoo import _, api, models, fields


class DHLShippingMethodCountry(models.Model):
    _name = "dhl.shipping.method.country"
    _description = "DHL Shipping Method Country"

    country_id = fields.Many2one(
        "res.country", string="Country"
    )
    price = fields.Float()

    delivery_carriers = fields.Many2one('delivery.carrier')

