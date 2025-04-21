# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,_ #type:ignore 
from odoo.exceptions import UserError #type:ignore
from datetime import datetime


class ShDoctorCommission(models.Model):
    _name = "sh.doctor.commission"

    name = fields.Char("Name")

    company_currency_id = fields.Many2one('res.currency', compute='_compute_company_currency_id')
    
    @api.depends_context('company')
    def _compute_company_currency_id(self):
        self.company_currency_id = self.env.company.currency_id

    sh_res_partner_id = fields.Many2one("res.partner")
    sh_so_id = fields.Many2one("sale.order", string="Reference Number", tracking=True, required=True)
    sh_so_id_patient_name = fields.Many2one("res.partner", string="Patient Name", tracking=True, required=True)

    sh_date = fields.Datetime(string='Date', tracking=True, required=True)
    sh_so_amount = fields.Monetary("Total Amount", currency_field='company_currency_id',required=True)
    sh_commission_type = fields.Many2one("sh.commission.type",string="Commission Type", tracking=True, required=True)

    sh_rate = fields.Selection([('fixed','Fixed'),('percent','Percentage')], string="Commission Rate",tracking=True, required=True)

    sh_total_commission = fields.Monetary(string="Dr.Commission", currency_field='company_currency_id', required=True)

    
