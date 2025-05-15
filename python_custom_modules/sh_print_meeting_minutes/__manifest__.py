# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
{
    'name':'Print Meeting Minutes',
    'version':'1.0',
    'sequence':1,
    'summary':'Print Meeting Minutes',
    'description':'Print Meeting Minutes',
    'depends':['base_setup','web','mail','calendar'],
    'data':[        
        'views/calendar_event_inherit_views.xml',
        'report/sh_print_meeting_time_template.xml',
        'report/sh_print_meeting_time_report.xml'
        ],

    'installable':True,
    'application':True,
    'license': 'LGPL-3',
}