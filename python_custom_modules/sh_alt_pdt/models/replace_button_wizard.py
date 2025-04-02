# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,_ #type:ignore
from odoo.exceptions import UserError #type:ignore


class replace_button_wizard(models.TransientModel):
    _name = "replace.button.wizard"

    product_id = fields.Many2one("product.product",string="Product",readonly=True)
    
    product_ids = fields.Many2many("product.product",string="Alternative Products")

    alt_product_id = fields.Many2one("product.product",string="Replacement Product",required=True)    

    sale_order_line_id = fields.Many2one("sale.order.line")

    @api.onchange('product_id')
    def _onchange_product_id(self):
        print("\n\n\n\n\n\n======",self.product_id)
        self.product_ids = self.product_id.alt_pdt_ids.ids


    def replace_action(self):
        print("\n\n\n\n\n\n=====In Replace",self.alt_product_id)
        self.sale_order_line_id.product_id = self.alt_product_id
        print("\n\n\n\n\n\n=====In Replace", self.sale_order_line_id.product_id)



