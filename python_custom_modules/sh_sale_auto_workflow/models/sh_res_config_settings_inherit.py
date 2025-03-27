# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,_ #type:ignore
from odoo.exceptions import UserError #type:ignore

class sh_res_config_settings(models.TransientModel):
    _inherit = 'res.config.settings'

    enable_auto_workflow = fields.Boolean(string="Enable Auto Sale Workflow")
    default_workflow = fields.Many2one("sh.sale.auto.workflow", string="Default Workflow")