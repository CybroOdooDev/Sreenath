from odoo import models, fields, api, _


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    # @api.onchange('identification_id')
    # def _onchange_identification_id(self):
    #     if self.identification_id:
    #         search

    _sql_constraints = [
        ('employee_code_unique', 'unique(identification_id)', 'Employee with same Identification Number already exists'),
    ]