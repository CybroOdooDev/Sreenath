# -*- coding: utf-8 -*-


{
    'name': 'Inventory Valuation By Location',
    'version': '16.0.1.0.0',
    'summary': 'Inventory Valuation By Location',
    'author': '',
    'website': "",
    'company': '',
    'category': '',
    'depends': ['base', 'contacts', 'sale_management', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/delivery_boy_views.xml',
        'views/delivery_boy_commission_views.xml',
        'views/stock_picking_views.xml',
        'wizard/assign_delivery_boy_views.xml',
        'views/res_partner_views.xml',
        'views/menu.xml',
        'views/sequence.xml',
    ],
    'images': [],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
}
