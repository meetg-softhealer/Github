# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
{
    'name':'SH Purchase Budget Limit',
    'version':'1.0',
    'sequence':1,
    'summary':'SH Purchase Budget Limit',
    'description':'SH Purchase Budget Limit',
    'depends':['base_setup','web','account_budget','purchase'],
    'data':[        
            'views/budget_analytic_views.xml'
        ],

    'installable':True,
    'application':True,
    'license': 'LGPL-3',
}