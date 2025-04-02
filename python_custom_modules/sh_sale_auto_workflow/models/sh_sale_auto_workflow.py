# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,_ #type:ignore
from odoo.exceptions import UserError #type:ignore

class sh_sale_auto_workflow(models.Model):
    _name = "sh.sale.auto.workflow"

    name = fields.Char(string="Name")

    delivery_order = fields.Boolean(string="Delivery Order")
    create_invoice = fields.Boolean(string="Create Invoice")
    validate_invoice = fields.Boolean(string="Validate Invoice",domain=[('validate_invoice','=',True)])
    register_payment = fields.Boolean(string="Register Payment",domain=[('register_payment','=',True)])
    invoice_by_mail = fields.Boolean(string="Send Invoice by Email",domain=[('validate_invoice','=',True)])

    company_id = fields.Many2one("res.company", string="Company", required=True)
    sale_journal = fields.Many2one("account.journal", string="Sale Journal",domain=[('type','=','sale')])
    payment_journal = fields.Many2one("account.journal", string="Payment Journal",domain=[('type','in',('bank','cash'))])
    
    