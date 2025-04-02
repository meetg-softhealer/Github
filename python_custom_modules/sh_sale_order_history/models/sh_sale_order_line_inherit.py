# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api #type:ignore
from odoo.exceptions import UserError, ValidationError #type:ignore

class sh_sale_order_lines_inherit(models.Model):
    _inherit = "sale.order.line"

    select_bool = fields.Boolean()
    sale_order_id = fields.Many2one("sale.order", string="Sale Order")

    sh_status = fields.Selection(related='order_id.state')

    def view_order_action(self):
        # record = self.env['sale.order'].browse['order_id']
        return {
            'type': 'ir.actions.act_window',            
            'res_model': 'sale.order',        
            'view_mode': 'form',
            'views_type': 'form',
            'view_id': self.env.ref('sale.view_order_form').id,
            'res_id': self.order_id.id,
        }