# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,_,Command #type:ignore
from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta 

class ShShiftAllocation(models.Model):
    _name = "sh.shift.allocation"

    name = fields.Char("", required=True)

    sh_change_shift_request_id = fields.Many2one("sh.change.shift.request")    
    sh_company_id = fields.Many2one("res.company", default=lambda self: self.env.company.id)
    sh_current_user = fields.Many2one("hr.employee", default=lambda self: self.env.user.id)
    sh_partner_ids = fields.Many2many("res.partner")
    sh_bool = fields.Boolean()
    sh_button_bool = fields.Boolean()
    sh_time = timedelta(days=1)

    sh_resource_calendar_id = fields.Many2one("resource.calendar", string="Shift Schedule", required=True)
    sh_employee_ids = fields.Many2many("hr.employee", string="Employees", required=True)
    # sh_shift_schedule_id = fields.Many2one("resource.calendar", string="Shift schedule")
    sh_shift_type_id = fields.Many2one("sh.shift.type", string="Shift Type", required=True)

    sh_from_date = fields.Datetime("From Date", required=True)
    sh_date = fields.Date("Sh Date", store=True)

    @api.onchange('sh_from_date')
    def _onchange_sh_from_date(self):
        if self.sh_from_date:
            self.sh_date = self.sh_from_date.date()
            # print("\n\n\n sh_date", self.sh_date)   

    # @api.depends('sh_from_date')
    # def _compute_sh_date(self):
    #     for record in self:
    #         record.sh_date = record.sh_from_date.date()
    #         print("\n\n\n\n sh_date",record.sh_date)

    sh_to_date = fields.Datetime("To Date", required=True)
    # sh_date = fields.Date(related='sh_from_date')
    sh_working_hours = fields.Float("Working Hours", related='sh_resource_calendar_id.hours_per_day')

    sh_scheduled_info_ids = fields.One2many("sh.scheduled.info", "sh_shift_allocation_id")

    sh_stage = fields.Selection([('draft','Draft'),('alloted','Alloted')], default='draft', readonly=True)
            
    sh_change_request_for_allocation_ids = fields.Many2many("sh.change.request.line", 
                                             "sh_shift_allocation_sh_change_shift_request_line_rel",
                                             "sh_shift_allocation_id",
                                             "sh_req_line_id",
                                            string="Change Requests"
                                            )
    
    def sh_send_shift_allocation_email(self):
        template = self.env.ref('sh_shift_management.sh_shift_allocation_template')
        template.send_mail(self.id, force_send=True)

    def sh_allocate_action(self):
        # sh_notify_ids = self.search([('sh_date','=',datetime.today().date()+relativedelta(days=self.sh_company_id.sh_days))])
        # print("\n\n\n sh_notify_ids", sh_notify_ids)        
        # # print("days", self.env.company.sh_days)
        # print("date left", self.sh_date)
        # print("date right", (datetime.today().date()+relativedelta(days=self.sh_company_id.sh_days)))

        # 10/0        
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
        
        record = self.env['sh.change.shift.request'].create({
            'name':self.name,
            'sh_shift_allocation_id':self.id,
            'sh_resource_calendar_id':self.sh_resource_calendar_id.id,
            'sh_employee_ids':self.sh_employee_ids.ids,
            'sh_from_date':self.sh_from_date,
            'sh_to_date':self.sh_to_date,
            'sh_shift_type_id':self.sh_shift_type_id.id,
              # 'sh_scheduled_info_ids':self.sh_scheduled_info_ids.ids
        })

        self.sh_change_shift_request_id = record.id
        self.sh_partner_ids = self.sh_employee_ids.mapped("user_id").mapped("partner_id")
        print("\n\n\n partner ids", self.sh_partner_ids)
        self.sh_button_bool = True
        self.sh_send_shift_allocation_email()

    def sh_send_shift_allocation_notification_email(self):        
        template = self.env.ref('sh_shift_management.sh_shift_allocation_notification_template')
        template.send_mail(self.id, force_send=True)

    # @api.model
    # def write(self, values):            
    
    #     result = super(ShShiftAllocation, self).create(values)
    #     print("\n\n\n values", values)
    #     print("\n\n\n sh_date", result['sh_date'])


    #     return result

    # def write(self, values):
    
    #     result = super(ShShiftAllocation, self).write(values)
    
    #     print("\n\n\n values", values)
    #     print("\n\n\n sh_date", result['sh_date'])

    #     return result
    



    def _cron_shift_notification(self):
        # print("\n\n\n\n cron self", self)
        # print("\n\n\n company id", self.sh_company_id.sh_days)
        # self.sh_date = datetime.strptime(self.sh_from_date, "%d%b%Y%")
        sh_notify_ids = self.env['sh.shift.allocation'].search([])
        # print("\n\n\n date", datetime.today().date())
        

        for rec in sh_notify_ids:
            print("\n\n\n rec", rec)
            

        print("\n\n\n sh_notify_ids", sh_notify_ids)        
        print("days", self.sh_company_id.sh_days)
        print("datetime", (datetime.today().date()+relativedelta(days=self.sh_company_id.sh_days)))

        for rec in sh_notify_ids:
            rec.sh_send_shift_allocation_notification_email()