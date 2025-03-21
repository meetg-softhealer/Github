# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api #type:ignore
from odoo.exceptions import UserError, ValidationError #type:ignore


class sale(models.Model):
    _name = "sh.sale"

    name = fields.Char(default="New")

    #make a group in xml
    partner_id = fields.Many2one("res.partner", string="Customer")

    #make a group in xml
    exp_date = fields.Date(string="Expiration")
    quote_date = fields.Date(string="Quotation Date")
    payment_terms_id = fields.Many2one("sale.order", string="Payment Terms")
    
    order_line_id = fields.Many2one("sale.order.line", string="")



    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _("New")) == _("New"):   #type:ignore
                seq_date = fields.Datetime.context_timestamp(
                    self, fields.Datetime.to_datetime(vals['date_order'])
                ) if 'date_order' in vals else None
                vals['name'] = self.env['ir.sequence'].with_company(vals.get('company_id')).next_by_code(
                    'sale.order', sequence_date=seq_date) or _("New") #type:ignore
