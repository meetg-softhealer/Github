# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
{
    'name':'SH Restrict Timesheet',
    'version':'1.0',
    'sequence':10,
    'summary':'SH Restrict Timesheet',
    'description':'SH Restrict Timesheet',
    'depends':['timesheet_grid','project','hr'],
    'data':['security/sh_restrict_timesheet_security.xml',
            'views/res_config_settings_inherit_views.xml'        
        ],

    'installable':True,
    'application':True,
    'license': 'LGPL-3',
}