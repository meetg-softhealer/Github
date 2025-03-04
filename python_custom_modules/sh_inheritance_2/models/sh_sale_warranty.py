# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo import models,fields,api #type:ignore
from odoo.exceptions import UserError, ValidationError #type:ignore

class sale_warranty(models.Model):
    _name = "sh.sale.warranty"

    name = fields.Char("Name")
    sale_order_id = fields.Many2one("sale.order", string="Sale Order Id")
    warranty_period = fields.Integer(string="Warranty Period(In Months)", default="12")
    warranty_expiry_date = fields.Datetime(string="Warranty Expiry Date", compute='_compute_warranty_expiry_date')
    
    
    @api.depends('sale_order_id')
    def _compute_warranty_expiry_date(self):
        for record in self:
            if record.sale_order_id:
                # print(record.sale_order_id.date_order)
                record.warranty_expiry_date = record.sale_order_id.date_order + relativedelta(months=record.warranty_period)
            else:
                record.warranty_expiry_date = False