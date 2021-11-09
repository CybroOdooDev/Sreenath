from odoo import api, fields, models, _
from odoo.tools import format_amount


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    label_notes = fields.Char(string='Label Notes', store=True)

class ProductProduct(models.Model):
    _inherit = 'product.product'

    label_notes = fields.Html(string='Label Notes', store=True)

class ProductLabelLayout(models.TransientModel):
    _inherit = 'product.label.layout'

    extra_html = fields.Html('Extra Content', compute="_compute_extra_html")

    def _compute_extra_html(self):
        for rec in self:
            products = self.env['product.template'].search([])
            for product in products:
                if product.label_notes:
                    rec.extra_html = product.label_notes





