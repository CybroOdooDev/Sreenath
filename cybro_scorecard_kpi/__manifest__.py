# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2021-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Cybrosys Techno Solutions(<https://www.cybrosys.com>)
#
#    You can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################
{
    'name': 'KPI Scorecard',
    'version': '15.0.1.0.0',
    'category': 'Accounting',
    'live_test_url': 'https://www.youtube.com/watch?v=peAp2Tx_XIs',
    'summary': """ """,
    'description': """
                   
                    """,
    'author': 'Cybrosys Techno Solutions, Odoo SA',
    'website': "https://www.cybrosys.com",
    'company': 'Cybrosys Techno Solutions',
    'maintainer': 'Cybrosys Techno Solutions',
    'depends': ['base', 'account', 'sale',],
    'data': [
        'security/ir.model.access.csv',
        'views/kpi_team_view.xml',

        # 'security/security.xml',

    ],
    'assets': {
        'web.assets_backend': [
            'cybro_scorecard_kpi/static/src/scss/style.scss',
            'cybro_scorecard_kpi/static/src/scss/account_asset.scss',
            'cybro_scorecard_kpi/static/lib/bootstrap-toggle-master/css/bootstrap-toggle.min.css',
            'cybro_scorecard_kpi/static/src/js/account_dashboard.js',
            'cybro_scorecard_kpi/static/lib/Chart.bundle.js',
            'cybro_scorecard_kpi/static/lib/Chart.bundle.min.js',
            'cybro_scorecard_kpi/static/lib/Chart.min.js',
            'cybro_scorecard_kpi/static/lib/Chart.js',
            'cybro_scorecard_kpi/static/lib/bootstrap-toggle-master/js/bootstrap-toggle.min.js',

        ],
        'web.assets_qweb': [
            'cybro_scorecard_kpi/static/src/xml/template.xml',
        ],
    },
    'license': 'LGPL-3',
    'images': ['static/description/banner.gif'],
    'installable': True,
    'auto_install': False,
    'application': True,
}

