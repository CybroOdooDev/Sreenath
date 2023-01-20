# -*- coding: utf-8 -*-
# Copyright (c) 2019-Present Droggol Infotech Private Limited. (<https://www.droggol.com/>)

from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    dr_survey_id = fields.Many2one(related='website_id.dr_survey_id', string='Surveys', readonly=False)
    ayrshare_api_key = fields.Char('Ayrshare API Key ')

    @api.model
    def get_values(self):
        """get values from the fields"""
        res = super(ResConfigSettings, self).get_values()
        params = self.env['ir.config_parameter'].sudo().get_param
        ayrshare_api_key = params('dr_social_website.ayrshare_api_key')
        res.update(ayrshare_api_key=ayrshare_api_key)
        return res

    def set_values(self):
        """Set values in the fields"""
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('dr_social_website.ayrshare_api_key', self.ayrshare_api_key)





    # onboarding = fields.Boolean(string="Onboarding Finished", default=False)
    #
    # @api.model
    # def get_values(self):
    #     """get values from the fields"""
    #     res = super(ResConfigSettings, self).get_values()
    #     params = self.env['ir.config_parameter'].sudo().get_param
    #     onboarding = params('dr_social_website.onboarding')
    #     print(onboarding, 'client_id_instagram')
    #     res.update(
    #         onboarding=onboarding,
    #     )
    #     return res
    # #
    # def set_values(self):
    #     """Set values in the fields"""
    #     super(ResConfigSettings, self).set_values()
    #     self.env['ir.config_parameter'].sudo().set_param('dr_social_website.onboarding', self.onboarding)
    #
    # def set_values_onboarding(self):
    #     self.env['ir.config_parameter'].sudo().set_param('dr_social_website.onboarding', True)
    #
    #

class Website(models.Model):
    _inherit = 'website'

    dr_survey_id = fields.Many2one('survey.survey', string='Surveys')

class ResUsers(models.Model):

    _inherit = "res.users"

    onboarding = fields.Boolean(string="Onboarding Finished", default=True)

