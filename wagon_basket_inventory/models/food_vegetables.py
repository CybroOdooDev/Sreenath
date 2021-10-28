from odoo import models, fields, api, _
import json
from odoo.tools import date_utils
import io

try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter


class FoodVegetables(models.TransientModel):
    _name = 'food.vegetable'

    fv_lines = fields.Many2many('food.vegetable.lines', string='Scanning Lines', compute='_compute_fv_lines',
                                store=True)
    name = fields.Char("Name", default='Name')
    cluster = fields.Selection([('fv', 'FV'), ('fmcg', 'FMCG'), ('cf', 'CF')],
                               default='fv', required=True, invisible=True)
    slot = fields.Selection([('s1', 'S1'), ('s2', 'S2'), ('s3', 'S3'), ('s4', 'S4')],
                            default='s1')

    def button_print(self):
        data = []
        for rec in self.fv_lines:
            rec.is_printed = True
            line_data = {
                'date': rec.date,
                'cluster': dict(rec._fields['cluster'].selection).get(self.cluster),
                'sku': rec.sku,
                'product_id': rec.product_id.name,
                'weight': rec.weight,
                'qty': rec.qty,
                'slot': dict(rec._fields['slot'].selection).get(self.slot)
            }
            data.append(line_data)
        return {
            'type': 'ir.actions.report',
            'data': {'model': 'food.vegetable',
                     'options': json.dumps(data,
                                           default=date_utils.json_default),
                     'output_format': 'xlsx',
                     'report_name': 'Excel Report',
                     },
            'report_type': 'xlsx'
        }

    def get_xlsx_report(self, data, response):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        head = workbook.add_format({'align': 'center', 'bold': True, 'font_size': '20px'})
        txt = workbook.add_format({'font_size': '10px'})
        sheet.merge_range('A1:F2', 'FV REPORT', head)
        date_head = workbook.add_format({'align': 'center', 'bold': True,
                                         'font_size': '10px'})
        cell_format = workbook.add_format(
            {'align': 'center', 'bold': True, 'bg_color': '#d3d3d3;',
             'border': 1
             })
        sheet.write(3, 0, 'Slot: ' + data[0].get('slot'), date_head)
        sheet.write(5, 0, 'Date', cell_format)
        sheet.write(5, 1, 'Cluster', cell_format)
        sheet.write(5, 2, 'EAN/SKU', cell_format)
        sheet.write(5, 3, 'Product', cell_format)
        sheet.write(5, 4, 'Weight', cell_format)
        sheet.write(5, 5, 'Quantity', cell_format)
        sheet.set_column(5, 0, 15)
        sheet.set_column(5, 1, 15)
        sheet.set_column(5, 2, 15)
        sheet.set_column(5, 3, 15)
        sheet.set_column(5, 4, 15)
        sheet.set_column(5, 5, 15)
        row = 6
        col = 0
        for val in data:
            sheet.write(row, col + 0, val['date'], txt)
            sheet.write(row, col + 1, val['cluster'], txt)
            sheet.write(row, col + 2, val['sku'], txt)
            sheet.write(row, col + 3, val['product_id'], txt)
            sheet.write(row, col + 4, val['weight'], txt)
            sheet.write(row, col + 5, val['qty'], txt)
            row += 1

        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()

    @api.depends('name', 'slot', 'cluster')
    def _compute_fv_lines(self):
        sub_type = self.env['product.subtype'].search([('subtype', '=', 'FV')], limit=1)
        for rec in self:
            rec.fv_lines = False
            sale_order_lines = self.env['sale.order.line'].search(
                [('order_id.del_date', '=', fields.Date.today()), ('order_id.slot', '=', rec.slot),
                 ('state', '!=', 'cancel'), ('is_checked_in_fv', '=', False)])
            sale_order_lines = sale_order_lines.filtered(lambda l: sub_type.id in l.product_id.product_tmpl_id.sub_ids.ids)

            line_ids = []
            for line in sale_order_lines:
                if not line.is_checked_in_fv:
                    new_line = sale_order_lines.filtered(lambda l: int(l.product_id) == line.product_id.id)
                    qty = 0
                    for l in new_line:
                        qty += l.product_uom_qty
                        l.is_checked_in_fv = True

                    fv_line = self.env['food.vegetable.lines'].search(
                        [('date', '=', line.order_id.del_date), ('slot', '=', line.order_id.slot),
                         ('product_id', '=', line.product_id.id), ('is_printed', '=', False)], limit=1)
                    if not fv_line:
                        fv_line = self.env['food.vegetable.lines'].create({
                            'date': line.order_id.del_date,
                            'cluster': 'fv',
                            'sku': line.product_id.barcode,
                            'product_id': line.product_id.id,
                            'slot': line.order_id.slot,
                            'weight': line.product_id.product_template_attribute_value_ids.filtered(
                                lambda attr: attr.attribute_id.name == 'Qty').name,
                        })
                    fv_line.qty = qty
            search = self.env['food.vegetable.lines'].search(
                [('slot', '=', rec.slot), ('date', '=', fields.Date.today()), ('is_printed', '=', False)])
            search = search.filtered(lambda each:sub_type.id in each.product_id.product_tmpl_id.sub_ids.ids)
            rec.fv_lines = search.ids


class FoodVegetablesLines(models.Model):
    _name = 'food.vegetable.lines'

    date = fields.Date(string='Date')
    cluster = fields.Selection([('fv', 'FV'), ('fmcg', 'FMCG'), ('cf', 'CF')],
                               default='fv', required=True)
    sku = fields.Char(string='EAN/SKU')
    product_id = fields.Many2one('product.product', string='Product')
    weight = fields.Char(string='Weight')
    qty = fields.Float(string='Quantity')
    is_printed = fields.Boolean(default=False)
    slot = fields.Selection([('s1', 'S1'), ('s2', 'S2'), ('s3', 'S3'), ('s4', 'S4')],
                            )


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    is_checked_in_fv = fields.Boolean(default=False, copy=False)
