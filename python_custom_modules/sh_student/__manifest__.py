# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
{
    'name':'SH Student',
    'version':'1.0',
    'sequence':6,
    'summary':'SH Student',
    'description':'SH Student',
    'depends':['base_setup','web','mail'],
    'data':[
        'security/ir.model.access.csv',
        'views/sh_student_views.xml',
        'views/sh_age_category_views.xml',
        'views/sh_student_menu.xml',
        'report/sh_student_report_template.xml',
        'report/sh_student_report.xml'
        ],

    'installable':True,
    'application':True,
    'license': 'LGPL-3',
}