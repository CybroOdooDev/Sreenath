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
#############################################################################py
{
    'name': "All in one Whatsapp",
    'version': '16.0.1.0.0',
    'summary': """Send whatsapp messages to the partner""",
    'description': """ This module helps you to send a whatsapp message to your partners that are in sale order, purchase order, 
        invoice and bills, and deliver orders.""",
    'author': 'Cybrosys Techno Solutions',
    'company': 'Cybrosys Techno Solutions',
    'maintainer': 'Cybrosys Techno Solutions',
    'category': 'Whatsapp',
    'depends': ['base','web', 'sale', 'stock', 'purchase','account','contacts'],
    'data': [
        'security/ir.model.access.csv',
        # 'security/sms_security.xml',
        'wizard/send_message_wizard.xml',
        'views/whatsapp_send_views.xml',
        'views/template.xml',
        'wizard/warning_message_wizard.xml',
    ],
    'images':['static/description/main.gif'],
    'license': "AGPL-3",
    'installable': True,
    'application': True,
}
