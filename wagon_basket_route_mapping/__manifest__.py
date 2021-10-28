# -*- coding: utf-8 -*-
{
    'name': "Wagon Route Mapping",
    'category': 'Sales',
    'version': '14.0.2.0.3',
    'author': 'Cybrosys Techno Solutions',
    'maintainer': 'Cybrosys Techno Solutions',
    'company': 'Cybrosys Techno Solutions',
    'website': 'https://www.cybrosys.com',
    'depends': [
        'base',
        'web_map',
        'sale_management',
        'stock',
        'purchase',
        'stock_barcode_picking_batch',
        'woo_commerce_connector'
    ],
    'data': [
        'data/route_mapping.xml',
        'security/ir.model.access.csv',
        'views/route_mapping.xml',
        'views/delivery_orders.xml',
        'views/sale_order.xml',
        'views/assets.xml',
    ],
'qweb':[
        "static/src/map.xml"
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
