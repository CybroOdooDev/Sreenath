from odoo import api, fields, models, _
from odoo.tools import format_amount


class ProductProduct(models.Model):
    _inherit = 'product.template'

    price_with_tax = fields.Float(string='Total price with tax', compute='get_tax_in_price')

    def get_tax_in_price(self):
        if self.taxes_id:
            taxes = self.taxes_id.compute_all(self.list_price)
            tax_amount = sum(t.get('amount', 0.0) for t in taxes.get('taxes', []))
            self.price_with_tax = self.list_price + tax_amount




