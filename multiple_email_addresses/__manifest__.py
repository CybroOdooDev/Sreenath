
{
    'name': "Multiple Email Addresses",
    'version': '14.0.1.0.0',
    'summary': """This module helps to add multiple email in contacts""",
    'description': """This module helps to add multiple email in contacts""",
    'category': '',
    'author': '',
    'company': '',
    'maintainer': '',
    'website': "",
    'depends': ['contacts', 'base'],

    'data': [
        'security/ir.model.access.csv',
        'views/email_addresses_views.xml',
    ],
    'license': "AGPL-3",
    'installable': True,
    'application': False,
}