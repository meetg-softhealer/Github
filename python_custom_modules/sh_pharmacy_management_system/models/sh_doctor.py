# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,_ #type:ignore
from odoo.exceptions import UserError #type:ignore

class ShDoctor(models.Model):
    _inherit = "res.partner"

    sh_is_doctor = fields.Boolean()

    sh_gender = fields.Selection(selection=[('male','Male'),('female','Female')],string="Gender")
    sh_specialization_ids = fields.Many2many("sh.specialization",string="Specialization")

    sh_commission_type = fields.Selection([('fixed','Fixed'),('percent','Percentage')], string="Commission Type",tracking=True)
    sh_amount = fields.Monetary("Amount", tracking=True)
    sh_commission_percent = fields.Float("Commission Rate(%)", tracking=True)


    