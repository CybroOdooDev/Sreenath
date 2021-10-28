from odoo import models, fields,api


class TrolleyLocation(models.Model):
    _name = 'trolley.location'
    _description = "Trolley Location"
    _rec_name = 'sequence'


    name = fields.Char(string="Location")
    company_id = fields.Many2one(
        'res.company', string="Company", readonly=True,
        index=True, default=lambda self: self.env.company)
    sequence = fields.Char(string='Location Reference', required=True,
                            copy=False, readonly=True,
                            index=True, default=lambda self: 'New')

    @api.model
    def create(self, vals):
        if vals.get('sequence', 'New' == 'New'):
            vals['sequence'] = self.env['ir.sequence'].next_by_code(
                'trolley.location.sequence' or 'New')
        result = super(TrolleyLocation, self).create(vals)
        return result