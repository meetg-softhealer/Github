# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,_ #type:ignore
from odoo.exceptions import UserError, ValidationError #type:ignore


class ShPurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def button_confirm(self):
        
        res = super(ShPurchaseOrder, self).button_confirm()        

        for record in self.order_line:        
            if record.analytic_distribution:    
                for rec_id in record.analytic_distribution:                
                    sh_rec = self.env['account.analytic.account'].browse(int(rec_id))                
                    sh_budget_line_ids = self.env['budget.line'].search([('account_id','=',sh_rec.id)])                               
                    for rec in sh_budget_line_ids:                    
                        if rec.account_id.name == sh_rec.name and rec.budget_analytic_state=='confirmed' and rec.budget_analytic_id.sh_allow_restrict=='restrict':                        
                            if rec.committed_amount > rec.budget_amount:                            
                                raise UserError("You don't have enough budget for the purchase !!!")                             
        return res
        