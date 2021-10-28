# -*- coding: utf-8 -*-
{
    'name': "Wagon Delivery",
    'category': 'Sales',
    'version': '14.0.0.0.5',
    'author': 'Cybrosys Techno Solutions',
    'maintainer': 'Cybrosys Techno Solutions',
    'company': 'Cybrosys Techno Solutions',
    'website': 'https://www.cybrosys.com',
    'depends': [
        'base',
        'sale_management',
        'stock',
        'purchase',
        'stock_barcode_picking_batch',
        'woo_commerce_connector',
        'wagon_basket_route_mapping'
    ],
    'data': [
        'data/operation_type.xml',
        'views/delivery_orders.xml',
        'views/stock_move_line.xml',
        'security/delivery_security.xml',
        'security/ir.model.access.csv',
        'wizard/delivery_return.xml',

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
