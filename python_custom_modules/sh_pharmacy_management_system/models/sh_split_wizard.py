# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,_ #type:ignore
from odoo.exceptions import UserError #type:ignore


class ShSplitWizard(models.TransientModel):
    _name = "sh.split.wizard"

    sh_order_line_ids = fields.Many2many("sale.order.line", string="Products")

    




        

