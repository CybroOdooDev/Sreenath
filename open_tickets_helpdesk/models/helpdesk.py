# -*- coding: utf-8 -*-

from odoo import api, fields, models


class HelpdeskTeam(models.Model):
    _inherit = "helpdesk.team"
    _description = "Helpdesk Team"

    open_tickets = fields.Integer(string='Open Tickets', compute='_compute_open_tickets')

    @api.depends('name')
    def _compute_open_tickets(self):
        ticket_data = self.env['helpdesk.ticket'].read_group(
            [('team_id', 'in', self.ids), ('stage_id.is_close', '=', False)], ['team_id'], ['team_id'])
        mapped_data = dict((data['team_id'][0], data['team_id_count']) for data in ticket_data)
        for rec in self:
            rec.open_tickets = mapped_data.get(rec.id, 0)
