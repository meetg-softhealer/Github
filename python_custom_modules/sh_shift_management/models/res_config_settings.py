# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,_ #type:ignore
from odoo.exceptions import UserError #type:ignore

class ShResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sh_enable_custom_shift = fields.Boolean("Enable Custom Shift Configuration", related='company_id.sh_enable_custom_shift', readonly=False)
    sh_restrict_checkout = fields.Boolean("Restrict heckout if working hours are not completed!!!", related='company_id.sh_restrict_checkout', readonly=False)
    sh_notify_shift = fields.Boolean("Notify Shift Allocation Before", related='company_id.sh_notify_shift', readonly=False)
    sh_days = fields.Integer("Days", related='company_id.sh_days', readonly=False)