# -*- coding: utf-8 -*-
# Copyright (c) 2019-Present Droggol Infotech Private Limited. (<https://www.droggol.com/>)

from odoo import models, fields


class ResPartner(models.Model):

    _inherit = 'res.partner'

    dr_social_account_count = fields.Integer(compute="_compute_dr_social_account_count")
    dr_social_posts_count = fields.Integer(compute="_compute_dr_social_posts_count")
    dr_survey_id = fields.Many2one('survey.user_input', string="Survey Answer")

    def _compute_dr_social_account_count(self):
        res = {
            r['dr_partner_id'][0]: r['dr_partner_id_count']
            for r in self.env['onyx.social.account'].read_group(
                domain=[('dr_partner_id', '!=', False)],
                fields=['dr_partner_id'],
                groupby=['dr_partner_id'],
            )
        }
        for partner in self:
            partner.dr_social_account_count = res.get(partner.id, 0)

    # Todo: use read_group for performace, whenever we need post count in the list/kanban view
    def _compute_dr_social_posts_count(self):
        for partner in self:
            social_accounts = self.env['onyx.social.account'].search([('dr_partner_id', '=', self.id)])
            partner.dr_social_posts_count = self.env['onyx.social.post'].search_count([('account_ids', 'in', social_accounts.ids)])

    def action_view_accounts(self):
        self.ensure_one()
        return {
            'name': f"{self.name}'s accounts",
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            "context": {"create": False},
            'res_model': 'onyx.social.account',
            'domain': [('dr_partner_id', '=', self.id)],
        }

    def action_view_posts(self):
        self.ensure_one()
        social_accounts = self.env['onyx.social.account'].search([('dr_partner_id', '=', self.id)])
        return {
            'name': f"{self.name}'s post",
            'type': 'ir.actions.act_window',
            'view_mode': 'kanban,tree,form',
            'res_model': 'onyx.social.post',
            'domain': [('account_ids', '=', social_accounts.ids)],
            'context': {'dr_active_account_ids': social_accounts.ids}
        }

    def action_redirect_survey_user_line(self):
        action = self.env["ir.actions.actions"]._for_xml_id("survey.action_survey_user_input")
        action['view_mode'] = 'tree'
        action['domain'] = ['&', '|', ('partner_id', 'in', self.ids), ('partner_id', 'in', self.child_ids.ids), ('state', '=', 'done')]
        return action
