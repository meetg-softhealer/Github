# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
{
    'name':'SH MRP Checklist',
    'version':'1.0',
    'sequence':10,
    'summary':'SH MRP Checklist',
    'description':'SH MRP Checklist',
    'depends':['mrp'],
    'data':[
        'security/sh_mrp_checklist_security.xml',
        'security/ir.model.access.csv',
        'views/sh_manufacturing_order_inherit_views.xml',
        'views/sh_mrp_checklist_views.xml',
        'views/sh_mrp_checklist_template_views.xml',
        'views/sh_mrp_checklist_menu.xml',
        'report/manufacturing_order_report_template.xml',
        'report/manufacturing_order_report.xml'
        ],

    'installable':True,
    'application':True,
    'license': 'LGPL-3',
}