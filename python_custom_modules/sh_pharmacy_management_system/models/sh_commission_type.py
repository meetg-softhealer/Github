# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,_ #type:ignore 
from odoo.exceptions import UserError #type:ignore

class ShCommissionType(models.Model):
    _name = "sh.commission.type"

    name = fields.Char("Commission Type")

