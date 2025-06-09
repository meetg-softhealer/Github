# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,_,Command #type:ignore

class ShApprovalConfig(models.Model):
    _name = "sh.approval.config"

    name = fields.Char("", required=True)

    sh_company_currency_id = fields.Many2one('res.currency', compute='_compute_company_currency_id')
    
    @api.depends_context('company')
    def _compute_company_currency_id(self):
        self.sh_company_currency_id = self.env.company.currency_id


    sh_min_amount = fields.Monetary("Minimum Amount", currency_field='sh_company_currency_id',required=True)

    sh_company_ids = fields.Many2many("res.company", string="Allowed Companies")

    sh_sales_person_bool = fields.Boolean("SalesPerson Always in CC")

    sh_approval_config_line_ids = fields.One2many("sh.approval.config.line", "sh_approval_config_id", string="")