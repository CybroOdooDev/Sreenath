# -*- coding: utf-8 -*-
{
    'name': 'Odoo Salla Integration',
    'version': '15.0.1.0.0',
    'summary': """ """,
    'description': """ """,
    'category': 'Tools',
    'author': 'Cybrosys Techno Solutions',
    'company': 'Cybrosys Techno Solutions',
    'maintainer': 'Cybrosys Techno Solutions',
    'depends': ['base', 'web', 'product', 'account', 'stock'],
    'website': 'https://www.cybrosys.com',
    'data': [
        'report/product_label_template.xml',
        'security/ir.model.access.csv',
        'views/product_view.xml',
        'views/salla_view.xml',
    ],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
