# Copyright 2021 Onestein (<https://www.onestein.nl>)
# License OPL-1 (https://www.odoo.com/documentation/14.0/legal/licenses.html#odoo-apps).

from odoo import api, models, fields


class DhlParcelItem(models.Model):
    _name = "dhl.parcel.item"
    _description = "DHL Parcel Items"
    _rec_name = "description"

    description = fields.Char(required=True)
    quantity = fields.Integer()
    weight = fields.Float()
    volume = fields.Float()
    value = fields.Float()
    hs_code = fields.Char()
    origin_country = fields.Char()
    product_id = fields.Char()
    properties = fields.Char()
    sku = fields.Char()
    return_reason = fields.Char()
    return_message = fields.Char()
    parcel_id = fields.Many2one("dhl.parcel", ondelete="cascade")


class DhlReturnParcelItem(models.Model):
    _name = "dhl.return.parcel.item"
    _description = "DHL Parcel Items"
    _rec_name = "return_description"

    return_description = fields.Char(required=True)
    return_quantity = fields.Integer()
    return_weight = fields.Float()
    return_volume = fields.Float()
    return_value = fields.Float()
    return_hs_code = fields.Char()
    return_origin_country = fields.Char()
    return_product_id = fields.Char()
    return_properties = fields.Char()
    return_sku = fields.Char()
    return_reason = fields.Char()
    return_message = fields.Char()
    return_parcel_id = fields.Many2one("dhl.return.parcel", ondelete="cascade")
