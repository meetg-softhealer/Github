# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,_ #type:ignore
from odoo.exceptions import UserError #type:ignore


class ShCashDrawerWizardLine(models.TransientModel):
    _name = "sh.cash.drawer.wizard.line"

    company_currency_id = fields.Many2one('res.currency', compute='_compute_company_currency_id')
    sh_session_id = fields.Many2one("pos.session")
    sh_date = fields.Date("Date")
    sh_cashier_id = fields.Many2one("res.users", string="Cashier")
    sh_open_bal = fields.Monetary(currency_field='company_currency_id')
    sh_close_bal = fields.Monetary(currency_field='company_currency_id')
    sh_cash_sale = fields.Monetary(currency_field='company_currency_id')
    sh_card_sale = fields.Monetary(currency_field='company_currency_id')
    sh_upi_sale = fields.Monetary(currency_field='company_currency_id')
    sh_net_cash = fields.Monetary(currency_field='company_currency_id')
    
    @api.depends_context('company')
    def _compute_company_currency_id(self):
        self.company_currency_id = self.env.company.currency_id