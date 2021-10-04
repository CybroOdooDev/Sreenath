# -*- coding: utf-8 -*-

{
    'name': "Installation Reports",
    'version': '14.0.1.0.0',
    'summary': """""",
    'description': """""",
    'category': 'Reports',
    'author': '',
    'company': '',
    'maintainer': '',
    'website': "",
    'depends': ['base', 'account','contacts'],
    'data': [
        'security/ir.model.access.csv',
        'views/tesco_installation_view.xml',
        'report/report_tesco_installation.xml',
        'report/report_tesco_installation_view.xml',


    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}