
{
    'name': "Email Re-directer",
    'version': '14.0.1.0.0',
    'summary': """This module helps to redirect email in helpdesk""",
    'description': """This module helps to redirect email in helpdesk""",
    'category': '',
    'author': '',
    'company': '',
    'maintainer': '',
    'website': "",
    'depends': ['helpdesk', 'base'],

    'data': [
        'security/ir.model.access.csv',
        'views/email_redirect_views.xml',
    ],
    'license': "AGPL-3",
    'installable': True,
    'application': False,
}