from odoo import models, fields


class Trolley(models.Model):
    _name = 'inventory.trolley'
    _description = "Trolley"

    name = fields.Char("Trolley")
    location_ids = fields.Many2many('trolley.location', string='Location')
    sequence = fields.Char(string='Sequence', required=True)
    barcode = fields.Char('Barcode')
    company_id = fields.Many2one(
        'res.company', string="Company", readonly=True,
        index=True, default=lambda self: self.env.company)

    _sql_constraints = [('barcode', 'unique(barcode)', 'Barcode must be unique!'),
                        ('sequence', 'unique(sequence)', 'Sequence must be unique!')]
