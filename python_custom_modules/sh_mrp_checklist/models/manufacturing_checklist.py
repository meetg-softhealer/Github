# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,_ #type:ignore
from odoo.exceptions import UserError #type:ignore

class ManufacturingChecklist(models.Model):
    _name = "manufacturing.checklist"

    
    name = fields.Char("Name", required=True)
    description = fields.Char("Description")

    company_id = fields.Many2one("res.company", string="Company", required=True)

    date = fields.Date("Date")  
    state = fields.Selection(string="State", selection=[('new','New'),('complete','Completed'),('cancel','Cancelled')],default='new')

    manufacturing_order_id = fields.Many2one("mrp.production")

    

