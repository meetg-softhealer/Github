# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,_ #type:ignore
from odoo.exceptions import UserError #type:ignore

class PurchaseOrderInherit(models.Model):
    _inherit = "purchase.order"

    vender_search = fields.Selection(selection=[('all','All'),('current_vendor','Current Vendor')], string="Vendor Wise search:")
    search_name = fields.Char(" ")
    search_filter = fields.Selection(selection=[('all','All'),
                                      ('name','Name'),
                                      ('internal_ref','Internal Reference'),
                                      ('barcode','Barcode'),
                                      ('vendor_product_name','Vendor Product Name'),
                                      ('vendor_product_code','Vendor Product Code'),
                                      ('attribute','Attribute'),
                                      ('attribute_value','Attribute Value')],
                                      string="Filter:")
    product_ids = fields.One2many("product.product","purchase_order_id")


    def load_products_action(self):   
        if self.vender_search=='all' and self.search_filter=='all' and self.search_name==False:
            # print("\n\n\n in method")      
            self.product_ids = self.env['product.product'].search([])
            # print("\n\n\n",self.product_ids)
        elif self.vender_search and self.search_filter:
            self.product_ids = self.env['product.supplierinfo'].search([('partner_id','=',self.partner_id.id)]).mapped('product_tmpl_id').mapped('product_variant_id')

        elif self.vender_search=='current_vendor':
            self.product_ids = self.env['product.supplierinfo'].search([('partner_id','=',self.partner_id.id)]).mapped('product_tmpl_id').mapped('product_variant_id')
            print("\n\n\n",self.product_ids)

    def add_selected_lines_action(self):
        record_list = [rec.multi_add_bool for rec in self.product_ids]

        if record_list:
            for record in self.product_ids:
                if record.multi_add_bool:
                    if record.id in self.env['purchase.order.line'].search([]).product_id.ids:
                        self.env['purchase.order.line'].search([('order_id','=',self.id),('product_id','=',record.id)]).product_qty += 1
                    else:               
                        record.env['purchase.order.line'].create({'order_id':self.id,
                                                        'product_id':record.id,                                                  
                                                        })
            self.product_ids.multi_add_bool = False
    
    def add_to_products_action(self):
        self.product_ids = self.env['product.product'].search([])

        for record in self.product_ids:
            if record.id in self.env['purchase.order.line'].search([]).product_id.ids:
                self.env['purchase.order.line'].search([('order_id','=',self.id),('product_id','=',record.id)]).product_qty += 1
            else:               
                record.env['purchase.order.line'].create({'order_id':self.id,
                                                'product_id':record.id,                                                  
                                                })