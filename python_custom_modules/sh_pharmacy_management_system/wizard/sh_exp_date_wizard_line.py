# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,_ #type:ignore
from odoo.exceptions import UserError #type:ignore
from datetime import datetime           
from dateutil.relativedelta import relativedelta

class ShExpiryDateWizardLine(models.TransientModel):
    _name = "sh.exp.date.wizard.line"

    sh_pdt_id = fields.Many2one("product.product", string="Product")
    sh_lot_name = fields.Char(string="Lot/Sr no.")
    sh_exp_date = fields.Datetime(string="Expiry Date")
    sh_days_remaining = fields.Integer(string="Days Remaining")
    
#     @api.depends('sh_exp_date')
#     def _compute_days_remaining(self):
#             self.sh_days_remaining = int(self.sh_exp_date.day() - datetime.today())
    
    sh_qty = fields.Float("Quantity")
    sh_category_id = fields.Many2one("product.category", string="Category")


