# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
{
    'name':'Relational Fields',
    'version':'1.0',
    'sequence':4,
    'summary':'Employee Time sheet Management',
    'description':'Employee Time Sheet And Attendance Management',
    'depends':['base_setup','web'],
    'data':[
        'security/ir.model.access.csv',
        'views/sh_diagnosis_views.xml',
        'views/sh_patient_views.xml',
        'views/sh_doctor_views.xml',
        'views/relation_menu.xml'
    ],
    'installable':True,
    'application':True,
    'license': 'LGPL-3',
}