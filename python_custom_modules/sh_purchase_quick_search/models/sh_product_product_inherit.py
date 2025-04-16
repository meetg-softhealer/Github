# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,_ #type:ignore
from odoo.exceptions import UserError #type:ignore

class ProductProductInherit(models.Model):
    _inherit = "product.product"

    purchase_order_id = fields.Many2one("purchase.order")
    multi_add_bool = fields.Boolean("Multi Add")

    def copy_product_order_line_action(self):
        order_line_ids = self.env['purchase.order.line'].search([('order_id','=',self.purchase_order_id.id)])
        print("\n\n\n\n\n====self id",self.id)
        print("\n\n\n\n\n====order line ids",order_line_ids.product_id.ids)
        
        if self.id in order_line_ids.product_id.ids:
            # order_line_ids.product_qty += 1
            self.env['purchase.order.line'].search([('order_id','=',self.purchase_order_id.id),('product_id','=',self.id)]).product_qty += 1
        else:
            self.env['purchase.order.line'].create({'order_id':self.purchase_order_id.id,  
                                                    'product_id':self.id
                                                })
        