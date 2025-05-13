# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,_ #type:ignore
from odoo.exceptions import UserError #type:ignore


class ShPatientWizardLine(models.TransientModel):
    _name = "sh.patient.wizard.line"

    sh_company_currency_id = fields.Many2one('res.currency', compute='_compute_company_currency_id')
    @api.depends_context('company_id')
    def _compute_company_currency_id(self):
        self.sh_company_currency_id = self.env.company.currency_id

    sh_so_id = fields.Many2one("sale.order", string="Order")
    sh_so_date = fields.Date("Order Date")
    sh_patient_id = fields.Many2one("res.partner", string="Patient")
    sh_age = fields.Integer("Age", related='sh_patient_id.sh_age')
    sh_gender = fields.Selection([('male','Male'),('female','Female')], string="Gender")
    sh_doctor_id = fields.Many2one("res.partner", string="Doctor", domain=[('sh_is_doctor','=',True)])
    sh_total_amount = fields.Monetary(currency_field='sh_company_currency_id', string="Total Amount")
