# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
{
    'name':'Sale Custom',
    'version':'1.0',
    'sequence':7,
    'summary':'Sale Custom',
    'description':'Sale Custom',
    'depends':['base_setup','web','mail','sale'],
    'data':[
        'security/ir.model.access.csv',
        'views/sh_sale_custom_views.xml',
        'views/sh_inherit_sale_order_views.xml',
        'views/sh_inherit_sale_order_line_views.xml',
        'views/sh_sale_custom_menu.xml'
        ],

    'installable':True,
    'application':True,
    'license': 'LGPL-3',
}