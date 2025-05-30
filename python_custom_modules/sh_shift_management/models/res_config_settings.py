# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,_ #type:ignore
from odoo.exceptions import UserError #type:ignore

class ShResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    sh_notify_shift = fields.Boolean("Notify Shift Allocation Before", related='company_id.sh_notify_shift', readonly=False)
    sh_days = fields.Integer("Days", related='company_id.sh_days', readonly=False)