# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
{
    'name':'SH Alternative Products',
    'version':'1.0',
    'sequence':16,
    'summary':'SH Alternative Products',
    'description':'SH Alternative Products',
    'depends':['base_setup','web','mail','sale_management','utm'],
    'data':[
        'security/sh_alt_pdt_security.xml',
        'security/ir.model.access.csv',
        'views/replace_button_wizard_views.xml',
        'views/sh_product_variant_inherit_views.xml',
        'views/sh_sale_order_inherit_views.xml',        
        ],

    'installable':True,
    'application':True,
    'license': 'LGPL-3',
}