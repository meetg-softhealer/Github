# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
{
    'name':'SH Mass Update',
    'version':'1.0',
    'sequence':1,
    'summary':'SH Mass Update',
    'description':'SH Mass Update',
    'depends':['base_setup','web','mail','sale_management'],
    'data':[                
        'security/ir.model.access.csv',
        'views/sale_order_views.xml',
        'views/sh_mass_update_views.xml',     
        'wizard/sh_mass_update_wizard_views.xml',
        'views/sh_mass_update_menu.xml'
        ],

    'installable':True,
    'application':True,
    'license': 'LGPL-3',
}