# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,_ #type:ignore
from odoo.exceptions import UserError #type:ignore

class sh_res_config_settings(models.TransientModel):
    _inherit = 'res.config.settings'

    group_enable_auto_workflow = fields.Boolean(string="Enable Auto Sale Workflow", related='company_id.enable_auto_workflow', readonly=False,
                                implied_group='sh_sale_auto_workflow.sh_sale_auto_workflow_enable')
    
    bydefault_workflow = fields.Many2one("sh.sale.auto.workflow", string="Default Workflow", related='company_id.bydefault_workflow', readonly=False)