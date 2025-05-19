# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,_ #type:ignore

class ShShiftAllocation(models.Model):
    _name = "sh.shift.allocation"

    sh_company_id = fields.Many2one("res.company", default=lambda self: self.env.company.id)
    sh_employee = fields.Many2many("hr.employee", string="Employee")
    sh_shift_schedule = fields.Many2one("resource.calendar", string="Shift schedule")
    sh_shift_type = fields.Many2one("sh.shift.type", string="Shift Type")

    sh_from_date = fields.Datetime("From Date")
    sh_to_date = fields.Datime("To Date")
    sh_working_hours = fields.Float("Working Hours")

    sh_stage = fields.Selection([('draft','Draft'),('alloted','Alloted')])

