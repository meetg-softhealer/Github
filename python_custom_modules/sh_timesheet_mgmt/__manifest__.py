# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
{
    'name':'Timesheet Management',
    'version':'1.0',
    'sequence':10,
    'summary':'Timesheet',
    'description':'Timesheet',
    'depends':['base_setup','web','mail'],
    'data':[
        'security/sh_timesheet_security.xml',
        'security/ir.model.access.csv',
        'views/sh_rejection_reason_views.xml',
        'views/sh_tag_views.xml',
        'views/sh_task_views.xml',
        'views/sh_timesheet_views.xml',
        'views/sh_timesheet_menu.xml'           
        ],

    'installable':True,
    'application':True,
    'license': 'LGPL-3',
}