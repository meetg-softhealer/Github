# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,_ #type:ignore
from odoo.exceptions import UserError, ValidationError #type:ignore
from dateutil.relativedelta import relativedelta
from datetime import datetime
from datetime import date

class shTimesheetInherit(models.Model):
    _inherit = "account.analytic.line"

    @api.model_create_multi
    def create(self, values):

        if not self.env.user.has_group('sh_restrict_timesheet.sh_timesheet_entry_access'):
            for rec in values:
                if not datetime.strptime(rec['date'], '%Y-%m-%d').date() >= (datetime.today()-relativedelta(days=self.env.company.restriction_days)).date():
                    raise UserError(f"You are not allowed to enter the timesheet before {self.env.company.restriction_days} days!!!")

        result = super(shTimesheetInherit, self).create(values)
      
        return result
    
    def write(self, values):
                
        if 'date' in values:
            if not self.env.user.has_group('sh_restrict_timesheet.sh_timesheet_entry_access'):
                if not datetime.strptime(values['date'], '%Y-%m-%d').date() >= (datetime.today()-relativedelta(days=self.env.company.restriction_days)).date():
                    raise UserError(f"You are not allowed to enter the timesheet before {self.env.company.restriction_days} days!!!")

        result = super(shTimesheetInherit, self).write(values)
    
        return result
    