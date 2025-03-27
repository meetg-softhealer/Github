# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,_ #type:ignore
from odoo.exceptions import UserError #type:ignore


class replace_button_wizard(models.TransientModel):
    _name = "replace.product.wizard"
    
    name = fields.many2one("product.product", string="Name",readonly=True)

    @api.model
    def default_get(self):
        active_id = self.env.context.get('active_id', []) # Get selected ticket IDs from context
        if active_id:
            rec = self.env['sale.order.line'].browse(active_id) # Fetch ticket records
            rec.write({'name': self.product_template_id})



