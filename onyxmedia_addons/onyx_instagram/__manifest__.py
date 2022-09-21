# -*- coding: utf-8 -*-
##############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#    Copyright (C) 2009-TODAY Cybrosys Technologies(<http://www.cybrosys.com>).
#    Author: Nilmar Shereef(<http://www.cybrosys.com>)
#    you can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    GENERAL PUBLIC LICENSE (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'lINKEDIN ONYX',
    'version': '15.0.1.0.0',
    'summary': 'LINKEDIN',
    'author': 'Cybrosys Techno Solutions',
    'website': "http://www.cybrosys.com",
    'company': 'Cybrosys Techno Solutions',
    'category': '',
    'depends': ['sale_management', 'purchase'],
    'data': [
        'data/social_media_instagram.xml',
        'security/ir.model.access.csv',
        # 'wizard/sale_cancel.xml',
        'views/model_instagram.xml',
        'views/res_config_settings.xml'
    ],

    'images': ['static/description/banner.png'],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
}
