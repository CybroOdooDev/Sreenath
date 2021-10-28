# -*- coding: utf-8 -*-
{
    'name': "QC",
    'category': 'Sales',
    'version': '14.0.1.1.6',
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
        'wagon_basket_delivery'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/qc.xml',
        'views/segregation.xml',
        "views/barcode_templates.xml",

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
