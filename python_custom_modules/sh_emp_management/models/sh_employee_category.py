# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import fields,models

class Employee_Category(models.Model):
    _name="sh.employee.category"
    _description="Employee Category"
    
    name=fields.Char(string="Name")
    active=fields.Boolean(string="Active")
    color=fields.Integer(string="Color")
    employee_ids=fields.Many2many("sh.employee",string="Employees")
    ref = fields.Char("ref")