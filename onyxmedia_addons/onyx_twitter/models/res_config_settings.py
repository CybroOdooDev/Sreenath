from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    consumer_key = fields.Char(string="Api Key")
    consumer_secret_key = fields.Char(string="Api Secret")
    # access_token = fields.Char(string='Access Token')
    # access_token_secret = fields.Char(string='Access Token Secret')

    @api.model
    def get_values(self):
        """get values from the fields"""
        res = super(ResConfigSettings, self).get_values()
        params = self.env['ir.config_parameter'].sudo().get_param
        # payment_type = params('payment_zillopay.payment_type') or 'capture'
        # cert_str = params('payment_zillopay.cert_str')
        twitter_consumer_key = params('onyx_twitter.consumer_key')
        twitter_consumer_secret_key = params('onyx_twitter.consumer_secret_key')
        print(twitter_consumer_key,'clied')
        res.update(
            consumer_key=twitter_consumer_key,
            consumer_secret_key=twitter_consumer_secret_key,
            # x509_cert=x509_cert,
            # payment_type=payment_type,
        )
        return res

    def set_values(self):
        """Set values in the fields"""
        super(ResConfigSettings, self).set_values()
        # self.env['ir.config_parameter'].sudo().set_param('payment_zillopay.payment_type', self.payment_type)
        # self.env['ir.config_parameter'].sudo().set_param('payment_zillopay.cert_str', self.cert_str)
        self.env['ir.config_parameter'].sudo().set_param('onyx_twitter.consumer_key', self.consumer_key)
        self.env['ir.config_parameter'].sudo().set_param('onyx_twitter.consumer_secret_key', self.consumer_secret_key)