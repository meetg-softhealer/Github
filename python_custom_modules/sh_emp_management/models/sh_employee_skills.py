# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
from odoo import models,fields

class Employee_Skill(models.Model):
    _name="sh.employee.skill"
    _description="Employee Skill"
    
    name=fields.Char()