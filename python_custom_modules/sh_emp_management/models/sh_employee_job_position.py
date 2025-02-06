# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
from odoo import models,fields

class Employee_Jobs(models.Model):
    _name="sh.employee.jobs"
    _description="Employee Job"
    
    name=fields.Char(string="Job Position",required=True)
    