# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models #type:ignore


class ResCompany(models.Model):
    _inherit = "res.company"

    enable_auto_workflow = fields.Boolean(string="Enable Auto Sale Workflow")
    bydefault_workflow = fields.Many2one("sh.sale.auto.workflow", string="Default Workflow")



