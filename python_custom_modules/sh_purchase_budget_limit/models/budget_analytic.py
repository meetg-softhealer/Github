# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,_ #type:ignore
from odoo.exceptions import UserError, ValidationError #type:ignore


class ShBudgetAnalytic(models.Model):
    _inherit = "budget.analytic"

    sh_allow_restrict = fields.Selection([('restrict','Restrict'),('allow','Allow')], string="Allow/Restrict Override Amount", default='restrict')

