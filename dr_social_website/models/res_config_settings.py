# -*- coding: utf-8 -*-
# Copyright (c) 2019-Present Droggol Infotech Private Limited. (<https://www.droggol.com/>)

from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    dr_survey_id = fields.Many2one(related='website_id.dr_survey_id', string='Surveys', readonly=False)


class Website(models.Model):
    _inherit = 'website'

    dr_survey_id = fields.Many2one('survey.survey', string='Surveys')
