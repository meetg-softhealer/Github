# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,_ #type:ignore
from odoo.exceptions import UserError #type:ignore


class ShProductWizardLine(models.TransientModel):
    _name = "sh.product.wizard.line"

    sh_company_currency_id = fields.Many2one('res.currency', compute='_compute_company_currency_id')
    @api.depends_context('company')
    def _compute_company_currency_id(self):
        self.sh_company_currency_id = self.env.company.currency_id

    sh_pdt_id = fields.Many2one("product.product", string="Product")
    sh_categ_id = fields.Many2one("product.category", string="Category")

    sh_qty_sold = fields.Float("Quantity Sold")
    sh_unit_price = fields.Monetary(currency_field='sh_company_currency_id', string="Unit Price/Sale Price")
    sh_total_sale = fields.Monetary(currency_field='sh_company_currency_id', string="Total Sale")

    sh_margin_rate = fields.Float("Margin Rate %")
    sh_total_margin = fields.Monetary(currency_field='sh_company_currency_id', string="Total Margin")
    sh_cost_price = fields.Monetary(currency_field='sh_company_currency_id', string="Cost Price")