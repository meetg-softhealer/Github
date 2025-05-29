# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,_ #type:ignore
from odoo.exceptions import UserError #type:ignore


class ShShiftReportWizardLine(models.TransientModel):
    _name = "sh.shift.report.wizard.line"

    sh_employee_id = fields.Many2one("hr.employee", string="Employee")
    sh_shift_schedule_id = fields.Many2one("resource.calendar", string="Shift Schedule")
    sh_date = fields.Date("Date")
    sh_shift_type_id = fields.Many2one("sh.shift.type", string="Shift Type")
    sh_working_hours = fields.Float("Working Hours", related='sh_shift_schedule_id.hours_per_day')
    sh_week_day = fields.Selection([('Sunday','Sunday'),
                                     ('Monday','Monday'),
                                     ('Tuesday','Tuesday'),
                                     ('Wednesday','Wednesday'),
                                     ('Thursday','Thursday'),
                                     ('Friday','Friday'),
                                     ('Saturday','Saturday')
                                     ], string="Day")
