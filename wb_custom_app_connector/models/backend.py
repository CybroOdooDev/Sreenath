from odoo import models, fields, api
import json
import requests


class ApiBackend(models.Model):
    _name = 'api.backend'
    _description = 'Tips4y Backend'

    API_URL = 'http://tr-ecom-be.herokuapp.com/api/v1/erp/'

    def _default_company(self):
        return self.env['res.company']._company_default_get('api.backend')

    name = fields.Char(
        required=True
    )
    company_id = fields.Many2one(
        comodel_name='res.company',
        string="Company",
        required=True,
        default=lambda self: self._default_company(),
    )

    username = fields.Char(
        string='Username',
        required=True
    )
    password = fields.Char(
        string='Password',
        required=True
    )
    token = fields.Char(
        readonly=True,
        help='Authentication token obtained with the login method',

    )

    active = fields.Boolean(string="Active")

    def login(self):
        url = "http://tr-ecom-be.herokuapp.com/api/v1/erp/login?username=%s&password=%s"%(str(self.username),str(self.password))
        print(type(self.password),type(self.username))

        payload = "{\n\"username\": \"%s\",\n\"password\": \"%s\"\n}"%(str(self.username),str(self.password))
        headers = {
            'Content-Type': 'application/json',
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        self.token = response.json()['token']







