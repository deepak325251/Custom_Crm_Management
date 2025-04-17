# -*- coding: utf-8 -*-
{
    'name': "Custom CRM Stage Management",
    'summary': "Automatically track stage Changes",
    'author': "Deepak Kumar",
    'category': 'CRM',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','crm'],
    'external_dependencies': {
        'python': ['workdays'],
    },

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/stage_history_security.xml',
        'views/crm_stage_history_view.xml',
        'views/crm_lead_stage_view.xml',
        'data/schedule_action.xml',
        # 'views/templates.xml',
    ],
}

