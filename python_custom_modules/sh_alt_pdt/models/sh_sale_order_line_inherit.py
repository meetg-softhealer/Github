# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,_ #type:ignore
from odoo.exceptions import UserError #type:ignore


class sh_sale_order_line_inherit(models.Model):
    _inherit = "sale.order.line"

    def replace_button_action(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Alternative Product'),   #type:ignore
            'res_model': 'replace.button.wizard',
            'target': 'new',
            'view_mode': 'form',
            'context':{'default_product_id':self.product_id.id,
                       'default_sale_order_line_id':self.id} 
                       
        }

