# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import fields,models

class Department(models.Model):
    _name="sh.department"
    _description="Employee Department"
    
    name=fields.Char(string="Name")
    active=fields.Boolean(string="Active")
    department_id=fields.Many2one("sh.department",string="Parent Department")
    employee_id=fields.Many2one("sh.employee",string="Employee")
    department_ids=fields.One2many("sh.department","department_id",string="Child Department")
    employee_ids=fields.One2many("sh.employee","department_id",string="Employees")
    job_ids=fields.One2many("sh.job","department_id",string="Jobs")