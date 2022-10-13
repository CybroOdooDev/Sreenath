from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    client_id = fields.Char(string="Client Id")
    client_secret = fields.Char(string="Client Secret")

    linkedin_message = fields.Text(string='Message')
    linkedin_image = fields.Char('Image')
    linkedin_access_token = fields.Char('Access Token')

    @api.model
    def get_values(self):
        """get values from the fields"""
        res = super(ResConfigSettings, self).get_values()
        params = self.env['ir.config_parameter'].sudo().get_param
        # payment_type = params('payment_zillopay.payment_type') or 'capture'
        # cert_str = params('payment_zillopay.cert_str')
        client_id_linkedin = params('onyx_linkedin.client_id')
        client_secret_linkedin = params('onyx_linkedin.client_secret')

        linkedin_message = params('onyx_linkedin.linkedin_message')
        linkedin_image = params('onyx_linkedin.linkedin_image')
        linkedin_access_token = params('onyx_linkedin.linkedin_access_token')

        res.update(
            client_id=client_id_linkedin,
            client_secret=client_secret_linkedin,
            linkedin_message=linkedin_message,
            linkedin_image=linkedin_image,
            linkedin_access_token=linkedin_access_token,
            # x509_cert=x509_cert,
            # payment_type=payment_type,
        )
        return res

    def set_values(self):
        """Set values in the fields"""
        super(ResConfigSettings, self).set_values()
        # self.env['ir.config_parameter'].sudo().set_param('payment_zillopay.payment_type', self.payment_type)
        # self.env['ir.config_parameter'].sudo().set_param('payment_zillopay.cert_str', self.cert_str)
        self.env['ir.config_parameter'].sudo().set_param('onyx_linkedin.client_id', self.client_id)
        self.env['ir.config_parameter'].sudo().set_param('onyx_linkedin.client_secret', self.client_secret)
        self.env['ir.config_parameter'].sudo().set_param('onyx_linkedin.linkedin_message', self.linkedin_message)
        self.env['ir.config_parameter'].sudo().set_param('onyx_linkedin.linkedin_image', self.linkedin_image)
        self.env['ir.config_parameter'].sudo().set_param('onyx_linkedin.linkedin_access_token', self.linkedin_access_token)
