# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import fields,models

class Resource_Calender(models.Model):
    _name="sh.resource.calendar"
    _description="Employee Activity"
    
    name=fields.Char(string="Name")
    active=fields.Boolean(string="Active")
    
    