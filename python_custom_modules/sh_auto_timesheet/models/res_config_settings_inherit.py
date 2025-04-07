# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,_ #type:ignore
from odoo.exceptions import UserError #type:ignore

class sh_res_config_settings(models.TransientModel):
    _inherit = 'res.config.settings'

    group_enable_bool = fields.Boolean("Create Timesheet",related='company_id.group_enable_bool',readonly=False, implied_group='sh_auto_timesheet.sh_auto_timesheet_enable')