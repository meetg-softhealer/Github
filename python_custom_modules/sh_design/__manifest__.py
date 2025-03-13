# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
{
    'name':'SH Design',
    'version':'1.0',
    'sequence':13,
    'summary':'SH Design',
    'description':'SH Design',
    'depends':['base_setup','web','mail'],
    'data':[
        "security/ir.model.access.csv",
        "views/sh_design_category_views.xml",
        "views/sh_design_type_views.xml",
        "views/sh_design_views.xml",
        "views/sh_design_menu.xml"
        ],

    'installable':True,
    'application':True,
    'license': 'LGPL-3',
}