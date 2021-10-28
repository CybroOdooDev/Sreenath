# -*- coding: utf-8 -*-
{
    'name': "Wb custom App Connector",
    'summary': """WB Custom App Connector V14""",
    'description': '',
    'category': 'Sales',
    'version': '14.0.5.0.8',
    'author': 'Cybrosys Techno Solutions',
    'maintainer': 'Cybrosys Techno Solutions',
    'company': 'Cybrosys Techno Solutions',
    'website': 'https://www.cybrosys.com',
    'depends': [
        'base',
        'stock',
        'sale_management',
        'account',
        'sale_coupon',
        'woo_commerce_connector',
        'base_geolocalize'
    ],
    'data': [
        'data/cron.xml',
        'security/ir.model.access.csv',
        'views/backend.xml'

    ],
    'images': [],
    "external_dependencies": {"python": ["WooCommerce", "django", "numpy"]},
    'installable': True,
    'application': True,
    'auto_install': False,
}
