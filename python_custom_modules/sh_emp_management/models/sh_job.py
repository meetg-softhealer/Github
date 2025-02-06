# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import fields,models

class Job(models.Model):
    _name="sh.job"
    _description="Employee Job"
    
    name=fields.Char(string="Job")
    active=fields.Boolean(string="Active")
    employee_id=fields.Many2one('sh.employee',string="Employee")
    partner_id=fields.Many2one('res.partner',string="Name")
    employee_ids=fields.One2many('sh.employee','job_id',string="Employees")
    department_id=fields.Many2one('sh.department',string="Departments")
    favorite_user_ids=fields.Many2many('res.users',string="Favorite User",relation='favorite_user_res_uses_job',column1='res_user_id',column2='favorite_user_ids')
    interviewers_ids=fields.Many2many('res.users',string="Interviewer Name",relation='interviewers_res_users_job',column1='res_user_id',column2='interviewer_ids')
    extended_interviewers_ids=fields.Many2many('res.users',string="Extended Interviewer Name",relation='extended_interviewer_res_users_job',column1='res_user_id',column2='extended_interviewer_ids')
    