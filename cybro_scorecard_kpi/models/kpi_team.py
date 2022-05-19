# -*- coding: utf-8 -*-

import calendar
import datetime
from datetime import datetime

from dateutil.relativedelta import relativedelta

from odoo.http import request
from odoo import api, fields, models, _
import requests


class SalesTeams(models.Model):
    _name = 'kpi.team'

    name = fields.Char('Name')
    age = fields.Char('Name')


