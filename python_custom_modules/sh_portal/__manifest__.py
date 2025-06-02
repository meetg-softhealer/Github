# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
{
    'name':'SH Portal',
    'version':'1.0',
    'sequence':1,
    'summary':'SH Portal',
    'description':'SH Portal',
    'depends':['sale_management',
               'portal',
               'website'
               ],
    'data':[        
            'security/ir.model.access.csv',
            'views/sh_portal_views.xml',
            'views/sh_portal_template.xml'
        ],
    
    'installable':True,
    'application':True,
    'license': 'LGPL-3',
}