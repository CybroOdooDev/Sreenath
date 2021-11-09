from odoo import api, fields, models, _
import requests


class OdooSalla(models.Model):
    _name = 'odoo.salla'

    name = fields.Char('Name')
    product = fields.Many2one('product.template', string='Product')

    @api.model
    def create(self, vals):
        for record in self:
            res = super(OdooSalla, self).write(vals)
            url = "https://api.salla.dev/admin/v2"
            response = requests.post(url=url,
                                     json={'loginId': 'alreshi@takamoltech.com', 'password': 'gcp_gcv4cax!jub2NTC'})

            session = requests.Session()
            response_data = response.json()
            dataaa_dict = response_data.get('data')
            token = dataaa_dict.get('authToken')
            if (response.status_code == 200):
                my_headers = {'Authorization': token}
                ###########################################################
                # get all the id of a community               
                myy_headers = {'Authorization': token,
                               'Content-type': 'multipart/form-data'}
                post_community = requests.post(url=url,
                                               headers=my_headers)
        return record
