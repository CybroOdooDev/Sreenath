# -*- coding: utf-8 -*-
{
    'name': 'Product price with tax in Barcode Labels',
    'version': '15.0.1.0.0',
    'summary': """Print user defined product labels with the tax amount.""",
    'description': """The module enables user to print customized product labels, Barcode, Barcode Generator, Barcode Label, Product Label, Product Barcode Generator, Product Barcode, Label Print, Product Label Print
                    """,
    'category': 'Tools',
    'author': 'Cybrosys Techno Solutions',
    'company': 'Cybrosys Techno Solutions',
    'maintainer': 'Cybrosys Techno Solutions',
    'depends': ['base', 'web', 'product', 'account', 'stock'],
    'website': 'https://www.cybrosys.com',
    'data': [
        'report/product_label_template.xml',
        'views/product_view.xml',
    ],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
