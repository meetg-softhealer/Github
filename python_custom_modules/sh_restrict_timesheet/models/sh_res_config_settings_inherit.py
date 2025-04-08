# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,_ #type:ignore
from odoo.exceptions import UserError #type:ignore

class sh_res_config_settings(models.TransientModel):
    _inherit = 'res.config.settings'

    restriction_days = fields.Integer("Restrict Timesheet After",related='company_id.restriction_days',readonly=False)