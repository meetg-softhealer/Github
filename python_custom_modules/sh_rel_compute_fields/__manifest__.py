# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
{
    'name':'Relational and Compute Fields',
    'version':'1.0',
    'sequence':2,
    'summary':'Relstional and Compute fields practice',
    'description':'Relational and Compute fields practice',
    'depends':['base_setup','web'],
    'data':[
        'security/ir.model.access.csv',
        'views/sh_rel_compute_views.xml'
        ],
    'installable':True,
    'application':True,
    'license': 'LGPL-3',
}