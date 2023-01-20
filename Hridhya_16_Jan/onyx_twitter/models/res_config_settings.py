from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    consumer_key = fields.Char(string="Api Key")
    consumer_secret_key = fields.Char(string="Api Secret")
    oauth_token = fields.Char(string="Oauth Token")
    oauth_verifier = fields.Char(string="Oauth Verifier")

    twitter_message = fields.Text(string='Message')
    twitter_message = fields.Text(string='Message')
    twitter_image = fields.Char('Image')
    twitter_access_token = fields.Char('Access Token')

    @api.model
    def get_values(self):
        """get values from the fields"""
        res = super(ResConfigSettings, self).get_values()
        params = self.env['ir.config_parameter'].sudo().get_param
        # payment_type = params('payment_zillopay.payment_type') or 'capture'
        # cert_str = params('payment_zillopay.cert_str')
        twitter_consumer_key = params('onyx_twitter.consumer_key')
        twitter_consumer_secret_key = params('onyx_twitter.consumer_secret_key')
        oauth_token = params('onyx_twitter.oauth_token')
        oauth_verifier = params('onyx_twitter.oauth_verifier')

        twitter_message = params('onyx_twitter.twitter_message')
        twitter_image = params('onyx_twitter.twitter_image')
        twitter_access_token = params('onyx_twitter.twitter_access_token')
        print(twitter_consumer_key, 'clied')
        res.update(
            consumer_key=twitter_consumer_key,
            consumer_secret_key=twitter_consumer_secret_key,
            oauth_token=oauth_token,
            oauth_verifier=oauth_verifier,

            twitter_message=twitter_message,
            twitter_image=twitter_image,
            twitter_access_token=twitter_access_token,
        )
        return res

    def set_values(self):
        """Set values in the fields"""
        super(ResConfigSettings, self).set_values()
        # self.env['ir.config_parameter'].sudo().set_param('payment_zillopay.payment_type', self.payment_type)
        # self.env['ir.config_parameter'].sudo().set_param('payment_zillopay.cert_str', self.cert_str)
        self.env['ir.config_parameter'].sudo().set_param('onyx_twitter.consumer_key', self.consumer_key)
        self.env['ir.config_parameter'].sudo().set_param('onyx_twitter.consumer_secret_key', self.consumer_secret_key)
        self.env['ir.config_parameter'].sudo().set_param('onyx_twitter.oauth_token', self.oauth_token)
        self.env['ir.config_parameter'].sudo().set_param('onyx_twitter.oauth_verifier', self.oauth_verifier)

        self.env['ir.config_parameter'].sudo().set_param('onyx_twitter.twitter_message', self.twitter_message)
        self.env['ir.config_parameter'].sudo().set_param('onyx_twitter.twitter_image', self.twitter_image)
        self.env['ir.config_parameter'].sudo().set_param('onyx_twitter.twitter_access_token', self.twitter_access_token)
