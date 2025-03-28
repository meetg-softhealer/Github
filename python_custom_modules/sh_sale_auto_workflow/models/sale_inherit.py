# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,_ #type:ignore
from odoo.exceptions import UserError #type:ignore

class sale_order_inherit(models.Model):
    _inherit = "sale.order"

    sale_workflow = fields.Many2one("sh.sale.auto.workflow", string="Sale Workflow")
    

    def action_confirm(self):
        rtn = super(sale_order_inherit, self).action_confirm()
        self.auto_start()

        return rtn

    def auto_start(self):
        
        print("\n\n\n\n\n\n\n===========autostart")
        obj = self.sale_workflow 
        
        if obj.delivery_order:
            self.env['stock.picking'].search([('origin','=',self.name)]).button_validate()
            
        if obj.create_invoice:

            self.env['sale.advance.payment.inv'].search([('self.id','in',sale_order_ids)])#.create_invoices()  


            