# -*- coding: utf-8 -*-
# Copyright (c) 2019-Present Droggol Infotech Private Limited. (<https://www.droggol.com/>)

{
    'name': 'Onyx Social Account',
    'description': 'Onyx Social Account',
    'author': '',
    'license': 'OPL-1',
    'depends': [
        'web', 'mail', 'iap', 'link_tracker'
    ],
    'data': [
        'security/ir.model.access.csv',
        # 'security/rules.xml',
        'security/security.xml',
        'data/cron.xml',
        'views/onyx_social_account.xml',

        'views/onyx_social_media.xml',
        'views/onyx_social_live_post_views.xml',

        'views/onyx_social_post_template_views.xml',
        'views/onyx_social_post_views.xml',

        # 'views/footer.xml',
        # 'views/social.xml',
        # 'views/search.xml',
        # 'views/content_calendar.xml',
        # 'views/revision_request.xml',
        # 'views/revision_request_2.xml',
    ],
    'application': True,
    'installable': True,
    # 'assets': {
    #     'web.assets_frontend': [
    #         # 'dr_social_website/static/src/js/bootstrap_min.js',
    #         # 'dr_social_website/static/src/js/content_tour.js',
    #         #
    #         # 'dr_social_website/static/src/scss/style.scss',
    #         #
    #         # 'dr_social_website/static/src/scss/content.scss',
    #         # 'dr_social_website/static/src/scss/bootstrap-datetimepicker.css',
    #         # 'dr_social_website/static/src/scss/datepicker.scss',
    #         # 'dr_social_website/static/src/scss/social.scss',
    #         # # 'dr_social_website/static/src/scss/social_content.scss',
    #         # 'dr_social_website/static/src/js/revision_request.js',
    #         # 'dr_social_website/static/src/js/bootstrap-datetimepicker.js',
    #         # 'dr_social_website/static/src/js/content_calendar.js',
    #         # 'dr_social_website/static/src/js/social_dialog.js',
    #         # 'dr_social_website/static/src/js/portal.js',
    #         # # 'dr_social_website/static/src/js/calender.js',
    #         # 'dr_social_website/static/src/js/calendar.js',
    #         # 'dr_social_website/static/src/js/datepicker-full.min.js',
    #         # 'dr_social_website/static/src/js/datepicker_full.js',
    #         # # 'dr_social_website/static/src/js/bootstrap_min.js',
    #     ],
    #     'web.assets_qweb': [
    #         # 'dr_social_website/static/src/xml/calendar.xml',
    #         # # 'dr_social_website/static/src/xml/revision_calendar.xml',
    #         # # 'dr_social_website/static/src/xml/search.xml',
    #
    #     ],
    # },
}
