# -*- coding: utf-8 -*-
# Copyright (c) 2019-Present Droggol Infotech Private Limited. (<https://www.droggol.com/>)

from odoo import models, api
from odoo import http
from odoo.http import request


class IrHttp(models.AbstractModel):

    _inherit = 'ir.http'

    @classmethod
    def _auth_method_user_sudo(cls):
        request.uid = request.session.uid
        if not request.uid:
            raise http.SessionExpiredException("Session expired")

        # if not request._env and request.env:
        #     request._env = request.env(su=True)

        if not request._env:
            context = {**request.session.context, 'default_dr_account_user_id': request.uid}
            request._env = api.Environment(request.cr, 1, context)
