# -*- coding: utf-8 -*-
# Copyright (c) 2019-Present Droggol Infotech Private Limited. (<https://www.droggol.com/>)

{
    'name': 'Droggol Social Extension',
    'description': 'Droggol Social Extension',
    'author': 'Droggol Infotech Private Limited',
    'license': 'OPL-1',
    'depends': [
        'web',
        'web_editor',
        'base',
        'website',
       
        'survey',
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/rules.xml',
        'security/security.xml',
        'data/client_approval.xml',
        'views/templates.xml',
        'views/login.xml',
        'views/sign_up.xml',
        'views/views.xml',
        'views/res_partner.xml',
        'views/res_config_settings.xml',
        'views/survey_templates.xml',
        'views/snippets.xml',
        'views/footer.xml',
        'views/social.xml',
        'views/search.xml',
        'views/content_calendar.xml',
        'views/revision_request.xml',
        'views/revision_request_2.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'dr_social_website/static/src/js/bootstrap_min.js',
            'dr_social_website/static/src/js/content_tour.js',

            'dr_social_website/static/src/scss/style.scss',

            'dr_social_website/static/src/scss/content.scss',
            'dr_social_website/static/src/scss/bootstrap-datetimepicker.css',
            'dr_social_website/static/src/scss/datepicker.scss',
            'dr_social_website/static/src/scss/social.scss',
            # 'dr_social_website/static/src/scss/social_content.scss',
            'dr_social_website/static/src/js/revision_request.js',
            'dr_social_website/static/src/js/bootstrap-datetimepicker.js',
            'dr_social_website/static/src/js/content_calendar.js',
            'dr_social_website/static/src/js/social_dialog.js',
            'dr_social_website/static/src/js/portal.js',
            # 'dr_social_website/static/src/js/calender.js',
            'dr_social_website/static/src/js/calendar.js',
            'dr_social_website/static/src/js/datepicker-full.min.js',
            'dr_social_website/static/src/js/datepicker_full.js',
            # 'dr_social_website/static/src/js/bootstrap_min.js',
        ],
        'web.assets_qweb': [
            'dr_social_website/static/src/xml/calendar.xml',
            # 'dr_social_website/static/src/xml/revision_calendar.xml',
            # 'dr_social_website/static/src/xml/search.xml',

        ],
    },
}
