# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
{
    'name':'SH Support Ticket',
    'version':'1.0',
    'sequence':15,
    'summary':'SH Support Ticket',
    'description':'SH Support Ticket',
    'depends':['base_setup','web','mail','account','utm'],
    'data':[
        'security/sh_support_ticket_security.xml',
        'security/ir.model.access.csv',
        'demo/demo_data.xml',
        'views/ir_cron.xml',
        'views/res_partner_inherit_views.xml',
        'views/res_users_inherit_views.xml',
        'views/account_move_inherit_views.xml',
        'views/support_ticket_wizard_views.xml',
        'views/sh_support_ticket_views.xml',
        'views/sh_support_ticket_menu.xml',
        ],

    'installable':True,
    'application':True,
    'license': 'LGPL-3',
}