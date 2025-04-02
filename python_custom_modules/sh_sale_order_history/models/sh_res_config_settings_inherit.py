# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,_ #type:ignore
from odoo.exceptions import UserError #type:ignore

class sh_res_config_settings(models.TransientModel):
    _inherit = 'res.config.settings'

    sh_last_no_of_orders = fields.Integer(string="Last No. Of Orders",related='company_id.sh_last_no_of_orders',readonly=False)
   
    # sh_stage_ids = fields.Many2many("temp.table", string="Stage",config_parameter='sh_sale_order_history.sh_stage_ids')
    # stages = fields.Selection(string='stages',selection=[('draft','Quotation'),('sent','Quotation Sent'),('sale','Sales Order')])
    
    sh_last_no_of_days = fields.Integer(string="Last No of Days",related='company_id.sh_last_no_of_days',readonly=False)

    sh_enable_reorder = fields.Boolean(string="Enable Reorder",related="company_id.sh_enable_reorder",readonly=False)

    sh_stage_ids = fields.Many2many("temp.table",string="Stages", related='company_id.sh_stage_ids',readonly=False)

    # use_invoice_terms = fields.Boolean(
    #     string='Default Terms & Conditions',
    #     config_parameter='account.use_invoice_terms')