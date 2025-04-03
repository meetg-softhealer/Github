{
    'name':'SH Sale Auto Workflow',
    'version':'1.0',
    'sequence':16,
    'summary':'SH Sale Auto Workflow',
    'description':'SH Sale Auto Workflow',
    'depends':['base_setup','web','mail','sale_management','stock','account','utm','sale_pdf_quote_builder','payment_demo'],
    'data':[
        'security/sh_sale_auto_workflow_security.xml',
        'security/ir.model.access.csv',
        'demo/demo_data.xml',
        'views/sh_res_config_settings_inherit_views.xml',
        'views/sh_sale_auto_workflow_views.xml',
        'views/sh_sale_auto_workflow_menu.xml',
        'views/sale_inherit_views.xml'
        ],

    'installable':True,
    'application':True,
    'license': 'LGPL-3',
}