# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
{
    'name':'Employee Management',
    'version':'1.0',
    'sequence':1,
    'summary':'Employee Time sheet Management',
    'description':'Employee Time Sheet And Attendance Management',
    'category':'Human Resources/Employees',
    'depends':['base_setup','web','mail'],
    'data':[
        'security/ir.model.access.csv',
        'views/sh_employee_view.xml',
        'views/sh_employee_jobs.xml',
        'views/sh_department_view.xml',
        'views/sh_job_view.xml',
        'views/sh_employee_category.xml',
        'views/sh_resource_calender_view.xml',
        'views/sh_employee_menu.xml',
        ],
    'images':['static/description/icon.png'],
    'installable':True,
    'application':True,
    'license': 'LGPL-3',
}