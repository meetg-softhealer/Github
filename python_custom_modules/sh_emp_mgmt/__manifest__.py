# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
{
    'name':'SH Employee',
    'version':'1.0',
    'sequence':12,
    'summary':'SH Employee',
    'description':'SH Employee',
    'depends':['base_setup','web','mail'],
    'data':[
        "security/sh_employee_security.xml",
        "security/ir.model.access.csv",
        "views/sh_employee_views.xml",
        "views/sh_employee_menu.xml"
        ],

    'installable':True,
    'application':True,
    'license': 'LGPL-3',
}