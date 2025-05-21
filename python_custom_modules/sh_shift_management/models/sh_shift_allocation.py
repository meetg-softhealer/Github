# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,_,Command #type:ignore
from datetime import datetime
from datetime import timedelta

class ShShiftAllocation(models.Model):
    _name = "sh.shift.allocation"

    name = fields.Char("", required=True)

    sh_company_id = fields.Many2one("res.company", default=lambda self: self.env.company.id)
    sh_bool = fields.Boolean()
    sh_button_bool = fields.Boolean()
    sh_time = timedelta(days=1)

    sh_resource_calendar_id = fields.Many2one("resource.calendar", string="Shift schedule", required=True)
    sh_employee_ids = fields.Many2many("hr.employee", string="Employees", required=True)
    # sh_shift_schedule_id = fields.Many2one("resource.calendar", string="Shift schedule")
    sh_shift_type_id = fields.Many2one("sh.shift.type", string="Shift Type", required=True)

    sh_from_date = fields.Datetime("From Date", required=True)
    sh_to_date = fields.Datetime("To Date", required=True)
    sh_working_hours = fields.Float("Working Hours", related='sh_resource_calendar_id.hours_per_day')

    sh_scheduled_info_ids = fields.One2many("sh.scheduled.info", "sh_shift_allocation_id")

    sh_stage = fields.Selection([('draft','Draft'),('alloted','Alloted')], default='draft', readonly=True)
            
    def sh_allocate_action(self):
        self.sh_stage = 'alloted'
        current_date = self.sh_from_date
        while current_date <= self.sh_to_date:
            if current_date.strftime("%A") not in [rec.name for rec in self.sh_resource_calendar_id.sh_days_ids]:
                self.sh_scheduled_info_ids = [Command.create({
                    'sh_date':current_date,
                    'sh_shift_type_id':self.sh_shift_type_id.id,
                    'sh_dayofweek':current_date.strftime("%A")
                })]
            
            current_date += self.sh_time
        
        self.sh_button_bool = True
        
    # @api.model_create_multi
    # def create(self, values):

    #     result = super(ShShiftAllocation, self).create(values)
    #     self.sh_bool = True
    #     self.sh_button_bool = True

    #     return result
    