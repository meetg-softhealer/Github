# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
{
    'name':'SH Shift Management',
    'version':'1.0',
    'sequence':1,
    'summary':'SH Shift Management',
    'description':'SH Shift Management',
    'depends':['base_setup','web','mail','hr'],
    'data':[
        'security/ir.model.access.csv',   
        'views/res_config_settings_views.xml',
        'views/sh_shift_type_views.xml',
        'views/sh_shift_allocation_views.xml',
        'views/resource_calendar_views.xml',
        'views/sh_shift_management_menu.xml'     
        ],

    'installable':True,
    'application':True,
    'license': 'LGPL-3',
}