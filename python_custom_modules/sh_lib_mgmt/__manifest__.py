# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
{
    'name':'Library Management System',
    'version':'1.0',
    'sequence':5,
    'summary':'Library Management',
    'description':'Library Management',
    'depends':['base_setup','web','mail'],
    'data':[
        'security/ir.model.access.csv',
        'views/sh_lib_book_views.xml',
        'views/sh_lib_category_views.xml',
        'views/sh_lib_member_views.xml',
        'views/sh_lib_menu.xml'
        ],
    'installable':True,
    'application':True,
    'license': 'LGPL-3',
}