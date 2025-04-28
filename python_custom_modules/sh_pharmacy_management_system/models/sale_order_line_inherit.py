# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,_ #type:ignore
from odoo.exceptions import UserError #type:ignore

class ShSaleOrderLineInherit(models.Model):
    _inherit = "sale.order.line"

    select_bool = fields.Boolean(" ")

    sh_expiry_date = fields.Date("Expiry Date", tracking=True, required=True)
    sh_lot_no = fields.Char("Lot/Sr No.", tracking=True, required=True)

    # @api.onchange('product_id')
    # def _onchange_product_id(self):
    #     # res = super(ShSaleOrderLineInherit, self)._onchange_product_id()
        
    #     current_rec = self.order_id

    #     for rec in current_rec.order_line:
    #         if rec.product_id.categ_id.sh_is_narcotic:
    #             current_rec.sh_is_narcotic = True
    #             print("\n\n\n current_rec.sh_is_narcotic", current_rec.sh_is_narcotic)


        # return res 