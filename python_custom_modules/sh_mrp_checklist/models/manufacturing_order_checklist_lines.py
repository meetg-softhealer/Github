# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,_ #type:ignore
from odoo.exceptions import UserError #type:ignore
from datetime import datetime

class ManufacturingOrderChecklistLine(models.Model):
    _name = "manufacturing.order.checklist.line"

    name = fields.Char("Name")
    manufacturing_order_id = fields.Many2one("mrp.production")

    checklist_id = fields.Many2one("manufacturing.checklist")

    description = fields.Char(related='checklist_id.description',string="Description",readonly=False)

    date = fields.Date(default=datetime.today())

    state = fields.Selection(string="State", selection=[('new','New'),('complete','Completed'),('cancel','Cancelled')],default='new')

    def complete_method_action(self):
        self.state = 'complete'

    def cancel_method_action(self):
        self.state = 'cancel'