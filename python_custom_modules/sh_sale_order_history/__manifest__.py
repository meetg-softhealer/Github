# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
{
    'name':'SH Sale Order History',
    'version':'1.0',
    'sequence':17,
    'summary':'SH Sale Order History',
    'description':'SH Sale Order History',
    'depends':['base_setup','web','mail','sale_management'],
    'data':[
        'security/ir.model.access.csv',
        'views/sale_order_inherit_views.xml',
        'views/sh_res_config_settings_inherit_views.xml',
        'views/sh_temp_table_views.xml'
        ],

    'installable':True,
    'application':True,
    'license': 'LGPL-3',
}