# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
{
    'name':'Relational Fields 2',
    'version':'1.0',
    'sequence':6,
    'summary':'Relational Fields 2',
    'description':'Relational Fields 2',
    'depends':['base_setup','web'],
    'data':[
        'security/ir.model.access.csv',
        'views/sh_res_partner_views.xml',
        'views/sh_product_product_views.xml',
        'views/sh_account_tax_views.xml',
        'views/sh_sale_order_views.xml',
        'views/sh_sale_order_line_views.xml',
        'views/relation2_menu.xml',

    ],
    'installable':True,
    'application':True,
    'license': 'LGPL-3',
}