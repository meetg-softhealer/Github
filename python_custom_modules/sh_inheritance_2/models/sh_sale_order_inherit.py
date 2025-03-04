# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api #type:ignore
from dateutil.relativedelta import relativedelta    
from odoo.exceptions import UserError, ValidationError #type:ignore

class sale_order_inherit(models.Model):
    _inherit = "sale.order"

    warranty_applicable = fields.Boolean("Warranty Applicable")
    warranty_period = fields.Integer("Warranty Period(In Months)", default=12)
    warranty_exp_date = fields.Datetime("Warranty Expiry Date")
    
    # @api.depends('warranty_period')
    # def _compute_warranty_exp_date(self):
    #     for record in self:
    #         record.warranty_exp_date = record.date_order + relativedelta(months=record.warranty_period) 
    
    @api.model_create_multi
    def create(self, vals_list):    
        for rec in vals_list:
            res = super(sale_order_inherit, self).create(vals_list)

            if rec["warranty_applicable"]:
                warranty_id = self.env['sh.sale.warranty'].create({'name':res.partner_id.name,'sale_order_id':res.id})
                res.warranty_exp_date = warranty_id.warranty_expiry_date
                
        return res
    
    def write(self, values):
        
        if 'warranty_applicable' in values:
            if values.get("warranty_applicable"):
                warranty_id = self.env['sh.sale.warranty'].create({'name':self.name,'sale_order_id':self.id})
                self.warranty_exp_date = warranty_id.warranty_expiry_date
            else:
                warranty_id = self.env['sh.sale.warranty'].search([('sale_order_id', '=', self.id)], limit=1)
                warranty_id.unlink()
                self.warranty_exp_date = False

        warranty_id = self.env['sh.sale.warranty'].search([('sale_order_id', '=', self.id)], limit=1)

        if values.get('warranty_period'):
            warranty_id.warranty_period = values.get('warranty_period')
            self.warranty_exp_date = warranty_id.warranty_expiry_date

        result = super(sale_order_inherit, self).write(values)
    
        return result
    
    @api.onchange('warranty_period')
    def _onchange_warranty_period(self):
       if self.warranty_period < 6:
           raise UserError("Warranty can't be less than 6 months") 
       
    