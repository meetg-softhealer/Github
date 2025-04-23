# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,_ #type:ignore
from odoo.exceptions import UserError #type:ignore

class ShSaleOrderLineInherit(models.Model):
    _inherit = "sale.order.line"

    select_bool = fields.Boolean(" ")

    sh_expiry_date = fields.Date("Expiry Date", tracking=True, required=True)
    sh_lot_no = fields.Char("Lot/Sr No.", tracking=True, required=True)