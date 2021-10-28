from odoo import models, fields, api, _
from odoo.exceptions import AccessError, UserError, ValidationError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    putaway_quantity = fields.Float('Putaway Quantity', compute='_compute_putaway_quantities',
                                    compute_sudo=False, digits='Product Unit of Measure')

    def _compute_putaway_quantities(self):
        for rec in self:
            rec.putaway_quantity = 0
            putaway = self.env['stock.putaway.rule'].search([])
            quantity_count = self.env['stock.quant'].search(
                [('product_id', 'in', putaway.product_id.ids), ('location_id', 'in', putaway.location_out_id.ids)])
            if quantity_count:
                total_quant = []
                for quantity in quantity_count:
                    total_quant.append(quantity.available_quantity)
                rec.putaway_quantity = sum(total_quant)

    def action_view_putaway_location(self):
        putaway = self.env['stock.putaway.rule'].search([])
        domain = [('product_id', 'in', putaway.product_id.ids), ('location_id', 'in', putaway.location_out_id.ids)]
        hide_location = not self.user_has_groups('stock.group_stock_multi_locations')
        hide_lot = all(product.tracking == 'none' for product in self)
        self = self.with_context(
            hide_location=hide_location, hide_lot=hide_lot,
            no_at_date=True, search_default_on_hand=True,
        )

        # If user have rights to write on quant, we define the view as editable.
        if self.user_has_groups('stock.group_stock_manager'):
            self = self.with_context(inventory_mode=True)
            # Set default location id if multilocations is inactive
            if not self.user_has_groups('stock.group_stock_multi_locations'):
                user_company = self.env.company
                warehouse = self.env['stock.warehouse'].search(
                    [('company_id', '=', user_company.id)], limit=1
                )
                if warehouse:
                    self = self.with_context(default_location_id=warehouse.lot_stock_id.id)
        # Set default product id if quants concern only one product
        if len(self) == 1:
            self = self.with_context(
                default_product_id=self.id,
                single_product=True
            )
        else:
            self = self.with_context(product_tmpl_ids=self.product_tmpl_id.ids)
        action = self.env['stock.quant']._get_quants_action(domain)
        action["name"] = _('Update Quantity')
        return action
