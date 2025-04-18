# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
{
    'name':'SH Pharmacy Management System',
    'version':'1.0',
    'sequence':1,
    'summary':'SH Pharmacy Management System',
    'description':'SH Pharmacy Management System',
    'depends':['sale_management',
               'purchase',
               'contacts',
               'stock',
               'point_of_sale',                          
               'hr',
               'fleet'],
    'data':[        
        'security/ir.model.access.csv',  
        'views/sh_res_partner_view_inherit.xml',
        'views/sh_specialization_views.xml',
        'views/sh_pharmacy_menu.xml'
        ],
    'images':['static/description/pharmacy.png'],
    'installable':True,
    'application':True,
    'license': 'LGPL-3',
}