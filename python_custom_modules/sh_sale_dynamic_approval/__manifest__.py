# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
{
    'name':'SH Sale dynamic Approval',
    'version':'1.0',
    'sequence':1,
    'summary':'SH Sale dynamic Approval',
    'description':'SH Sale dynamic Approval',
    'depends':['mail','sale_management','account'],
    'data':[
            'security/ir.model.access.csv',
            'security/security.xml',
            'data/sh_submit_for_approval_mail_template.xml',
            'data/sh_reject_approval_mail_template.xml',
            'data/sh_confirm_order_mail_template.xml',
            'wizard/sh_reject_action_wizard_views.xml',
            'views/sale_order_views.xml',            
            'views/sh_approval_config_views.xml',
            'views/sh_approval_config_line_views.xml',            
            'views/sale_menus.xml'
        ],

    'installable':True,
    'application':True,
    'license': 'LGPL-3',
}