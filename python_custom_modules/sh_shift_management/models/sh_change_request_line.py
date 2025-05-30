# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,_,Command #type:ignore
from datetime import datetime
from datetime import timedelta

class ShChangeRequestLine(models.Model):
    _name = "sh.change.request.line"

    name = fields.Char("Name")        

    sh_company_id = fields.Many2one("res.company", default=lambda self: self.env.company.id)

    sh_allocation_id = fields.Many2one("sh.change.shift.request", string="Allocation Name")
    sh_resource_calendar_id = fields.Many2one("resource.calendar", string="Shift schedule")
    sh_employee_id = fields.Many2one("hr.employee", string="Employee")
    sh_shift_type = fields.Many2one("sh.shift.type", string="Shift Type")
    sh_from_date = fields.Datetime("From Date")
    sh_to_date = fields.Datetime("To Date")
    sh_working_hours = fields.Float("Working Hours")

    def sh_send_approval_email(self):
        template = self.env.ref('sh_shift_management.sh_change_request_approve_template')
        template.send_mail(self.id, force_send=True)

    def sh_send_rejection_mail(self):
        template = self.env.ref('sh_shift_management.sh_change_request_reject_template')
        template.send_mail(self.id, force_send=True)

    def sh_approve_request_action(self):       
        
        self.sh_allocation_id.sh_shift_allocation_id.sh_change_request_for_allocation_ids = [(4,self.id)]
        self.sh_allocation_id.sh_change_request_line_ids = [(3,self.id)]
        self.sh_send_approval_email()

    def sh_reject_request_action(self):
        self.sh_send_rejection_mail()        
        self.sh_allocation_id.sh_change_request_line_ids = [(2,self.id)]