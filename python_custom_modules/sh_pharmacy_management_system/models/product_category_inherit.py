# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,_ #type:ignore
from odoo.exceptions import UserError #type:ignore

class ShProductCategoryInherit(models.Model):
    _inherit = "product.category"

    sh_is_medicine = fields.Boolean("Is Medicine")