# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,_ #type:ignore
from odoo.exceptions import UserError #type:ignore


class ShCashDrawerWizardLine(models.TransientModel):
    _name = "sh.doctor.commission.wizard.line"

    sh_company_currency_id = fields.Many2one('res.currency', compute='_compute_company_currency_id')
    @api.depends_context('company_id')
    def _compute_company_currency_id(self):
        self.sh_company_currency_id = self.env.company.currency_id

    sh_so_id = fields.Many2one("sale.order", string="Sale Order")
    sh_date = fields.Date("Date")
    sh_doctor_id = fields.Many2one("res.partner", string="Doctor")
    sh_patient_id = fields.Many2one("res.partner", string="Patient")

    sh_bill_total = fields.Monetary(string="Bill Total", currency_field='sh_company_currency_id')

    sh_commission_percentage = fields.Float("Commission Percentage", default=0)

    sh_commission_fixed_amount = fields.Monetary(string="Fixed Commission Amount", currency_field='sh_company_currency_id', default=0)

    sh_com_amount = fields.Monetary(string="Total Commission", currency_field='sh_company_currency_id')