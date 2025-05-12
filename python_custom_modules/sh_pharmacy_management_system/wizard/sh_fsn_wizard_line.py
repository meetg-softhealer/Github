# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,_ #type:ignore
from odoo.exceptions import UserError #type:ignore


class ShFsnWizardLine(models.TransientModel):
    _name = "sh.fsn.wizard.line"

    sh_pdt_id = fields.Many2one("product.product", string="Product")
    sh_categ_id = fields.Many2one("product.category", string="Category")
    sh_stock_qty = fields.Float("Stock Qty")
    sh_stock_forecast = fields.Float("Stock Forecast")
    sh_qty_sold = fields.Float("Quantity Sold")
    sh_sold_rate = fields.Selection([('fast','Fast'),('slow','Slow')], string="Sale Rate:")  
    
    