# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
from datetime import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
from odoo import models,fields,api,_ #type:ignore
from odoo.exceptions import UserError, ValidationError #type:ignore

class sh_timesheet(models.Model):
    _name = "sh.timesheet"

    user_id = fields.Many2one("res.users", string="User", default = lambda self: self.env.user)
    name = fields.Char(string="Name")
    description = fields.Html(string="Description")
    date = fields.Date(string="Date", default = date.today())
    hours = fields.Float(string="Hours", widget = "float_time")
    tag_ids = fields.Many2many("sh.tag", string="Tag")
    state = fields.Selection([('draft', 'Draft'), ('submitted', 'Submitted'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='draft')
    # rejection_reason = fields.Text(string="Rejection Reason")
    task_ids = fields.One2many("sh.task", "timesheet_id",string="Tasks")
    total_amount = fields.Float(string="Total", compute='_compute_total_amount')
    reject_reason = fields.Char(string="Rejection Reason")
    
    @api.depends("task_ids")
    def _compute_total_amount(self):
        for record in self:
            sum = 0
            # print("\n\n\n\===================")
            for rec in record.task_ids:
                #iterating the loop 3rd time because there are multiple tasks so to iterate it over it
                # print("\n\n\n================",rec.task_ids)
                sum += rec.amount        
            record.total_amount = sum
        
    def approve_action(self):
        self.state = 'approved'

    def submit_action(self):
        self.state = 'submitted'

    def reject_action_wizard(self):
        # self.state = 'rejected'
        return {
            'type': 'ir.actions.act_window',
            'name': _('Rejection Reason'),   #type:ignore
            'res_model': 'sh.rejection.reason',
            'target': 'new',
            'view_mode': 'form',
            'views_type': 'form',
        }
    
    