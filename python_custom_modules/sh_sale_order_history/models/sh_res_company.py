# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models #type:ignore


class ResCompany(models.Model):
    _inherit = "res.company"

    sh_last_no_of_orders = fields.Integer(string="Last No. Of Orders")
    
    sh_last_no_of_days = fields.Integer(string="Last No of Days",default=1)

    sh_enable_reorder = fields.Boolean(string="Enable Reorder")

    sh_stage_ids = fields.Many2many("temp.table",string="Stages")



