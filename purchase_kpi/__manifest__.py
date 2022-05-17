# -*- coding: utf-8 -*-
{
    'name' : 'Product Sale/Purchase Information',
    'version' : '1.1',
    'summary': '',
    'sequence': 10,
    'description': """ Product Sale/Purchase Information""",
    'category': '',
    'website': '',
    'depends': ['base_setup', 'base', 'purchase', 'sale', 'stock'],
    'data': [
        "views/purchase_product_views.xml",
        "views/asset.xml",
    ],
    'demo': [],
    'qweb': ["static/src/xml/action_button.xml"],

    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
