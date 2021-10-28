from odoo import models, fields, api,_


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('product_id')
    def _onchange_product(self):
        print("produc", self.product_id.read())

        self.price_unit = self.product_id.lst_price if self.product_id.lst_price > 0 else self.product_id.list_price

