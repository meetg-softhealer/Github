# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
{
    'name':'SH Website',
    'version':'1.0',
    'sequence':2,
    'summary':'SH website',
    'description':'SH website',
    'depends':['base_setup','web','mail','website','contacts'],
    'data':[
            'views/sh_website_form_menu.xml',
            'views/sh_website_form_template.xml'
        ],

    'installable':True,
    'application':True,
    'license': 'LGPL-3',
}