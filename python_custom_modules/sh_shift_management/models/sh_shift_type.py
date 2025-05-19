# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,_ #type:ignore

class ShShiftType(models.Model):
    _name = "sh.shift.type"

    name = fields.Char("Shift Type Name")
    
    sh_company_id = fields.Many2one("res.company", default=lambda self: self.env.company.id)