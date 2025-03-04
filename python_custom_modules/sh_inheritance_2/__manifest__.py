# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
{
    'name':'SH Inheritance 2',
    'version':'1.0',
    'sequence':10,
    'summary':'SH Inheritance 2',
    'description':'SH Inheritance 2',
    'depends':['base_setup','web','mail','sale'],
    'data':[
        'security/ir.model.access.csv',
        'views/sh_sale_warranty_views.xml',
        'views/sh_sale_order_inherit_views.xml',
        'views/sh_inheritance_2_menu.xml'
        ],

    'installable':True,
    'application':True,
    'license': 'LGPL-3',
}