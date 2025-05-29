# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
{
    'name':'SH Shift Management',
    'version':'1.0',
    'sequence':1,
    'summary':'SH Shift Management',
    'description':'SH Shift Management',
    'depends':['base_setup','web','mail','hr','contacts'],
    'data':[
        'security/sh_shift_management_security.xml',
        'security/ir.model.access.csv',   
        'data/sh_shift_allocation_template.xml',
        'data/sh_shift_allocation_notification_template.xml',
        'data/sh_change_request_email_approval_template.xml',
        'data/sh_change_request_reject_template.xml',
        'report/sh_shift_report_template.xml',
        'report/sh_shift_report.xml',
        'views/ir_cron.xml',
        'views/res_config_settings_views.xml',
        'views/sh_days_views.xml',
        'views/sh_shift_type_views.xml',
        'views/sh_shift_allocation_views.xml',
        'views/sh_change_shift_request_views.xml',
        'views/resource_calendar_views.xml',
        'wizard/sh_update_allocation_wizard_views.xml',
        'wizard/sh_shift_report_wizard_views.xml',
        'views/sh_shift_management_menu.xml'     
        ],

    'installable':True,
    'application':True,
    'license': 'LGPL-3',
}