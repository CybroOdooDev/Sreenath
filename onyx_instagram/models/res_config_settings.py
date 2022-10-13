from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    client_id_instagram = fields.Char(string="Client Id")
    client_secret_instagram = fields.Char(string="Client Secret")

    @api.model
    def get_values(self):
        """get values from the fields"""
        res = super(ResConfigSettings, self).get_values()
        params = self.env['ir.config_parameter'].sudo().get_param
        # payment_type = params('payment_zillopay.payment_type') or 'capture'
        # cert_str = params('payment_zillopay.cert_str')
        client_id_instagram = params('onyx_instagram.client_id_instagram')
        client_secret_instagram = params('onyx_instagram.client_secret_instagram')
        print(client_id_instagram,'client_id_instagram',client_secret_instagram)
        res.update(
            client_id_instagram=client_id_instagram,
            client_secret_instagram=client_secret_instagram,
            # x509_cert=x509_cert,
            # payment_type=payment_type,
        )
        return res

    def set_values(self):
        """Set values in the fields"""
        super(ResConfigSettings, self).set_values()
        # self.env['ir.config_parameter'].sudo().set_param('payment_zillopay.payment_type', self.payment_type)
        # self.env['ir.config_parameter'].sudo().set_param('payment_zillopay.cert_str', self.cert_str)
        self.env['ir.config_parameter'].sudo().set_param('onyx_instagram.client_id_instagram', self.client_id_instagram)
        self.env['ir.config_parameter'].sudo().set_param('onyx_instagram.client_secret_instagram', self.client_secret_instagram)