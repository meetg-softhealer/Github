# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,_,Command #type:ignore
from odoo.exceptions import UserError #type:ignore

class ShApprovalConfig(models.Model):
    _name = "sh.approval.config"

    name = fields.Char("", required=True)

    sh_company_id = fields.Many2one("res.company", default=lambda self:self.env.company.id)

    sh_company_currency_id = fields.Many2one('res.currency', compute='_compute_company_currency_id')
    
    @api.depends_context('company')
    def _compute_company_currency_id(self):
        self.sh_company_currency_id = self.env.company.currency_id


    sh_min_amount = fields.Monetary("Minimum Amount", currency_field='sh_company_currency_id',required=True)

    sh_company_ids = fields.Many2many("res.company", string="Allowed Companies", required=True)

    sh_sales_person_bool = fields.Boolean("SalesPerson Always in CC")

    sh_approval_config_line_ids = fields.One2many("sh.approval.config.line", "sh_approval_config_id", string="", required=True)

    
    @api.model
    def create(self, values):
            
        result = super(ShApprovalConfig, self).create(values)
        if not result['sh_approval_config_line_ids']:
            raise UserError("Enter the approval levels for the configurations!!!")

        if not result['sh_approval_config_line_ids'].sh_user_ids.ids and not result['sh_approval_config_line_ids'].sh_group_ids.ids:
            raise UserError("Enter the approval level's users or groups for the configurations!!!")

        else:
            return result
    
    def write(self, values):
    
        result = super(ShApprovalConfig, self).write(values)
        if not self.sh_approval_config_line_ids:
            raise UserError("Enter the approval levels for the configurations!!!")
        
        if not self.sh_approval_config_line_ids.sh_user_ids.ids and not self.sh_approval_config_line_ids.sh_group_ids.ids:
            raise UserError("Enter the approval level's users or groups for the configurations!!!")

        else:
            return result
    