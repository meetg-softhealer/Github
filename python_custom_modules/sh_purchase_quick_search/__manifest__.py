# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
{
    'name':'SH Purchase Quick Product Search',
    'version':'1.0',
    'sequence':10,
    'summary':'Purchase Quick Product Searcht',
    'description':'Purchase Quick Product Search',
    'depends':['purchase','stock'],
    'data':[
        'security/sh_purchase_quick_search_security.xml',
        'security/ir.model.access.csv',
        'views/product_product_inherit_views.xml',
        'views/purchase_order_inherit_views.xml',
        ],
    'installable':True,
    'application':True,
    'license': 'LGPL-3',
}