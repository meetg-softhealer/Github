# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
{
    'name':'SH Auto Timesheet',
    'version':'1.0',
    'sequence':10,
    'summary':'SH Auto Timesheet',
    'description':'SH Auto Timesheet',
    'depends':['timesheet_grid','project','calendar'],
    'data':[
        'security/ir.model.access.csv',
        'views/sh_calender_form_inherit_views.xml'
        ],

    'installable':True,
    'application':True,
    'license': 'LGPL-3',
}