from odoo import models, fields, api, _
from odoo.exceptions import UserError


class StockPickingBatchInherit(models.Model):
    _inherit = 'stock.picking.type'

    add_product = fields.Boolean(string='Enable Add Product', default=True)
    put_in_pack = fields.Boolean(string='Enable Put in Pack', default=True)



