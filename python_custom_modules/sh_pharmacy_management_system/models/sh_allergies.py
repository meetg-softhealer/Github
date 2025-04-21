# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,_ #type:ignore 
from odoo.exceptions import UserError #type:ignore

class ShAllergies(models.Model):
    _name = "sh.allergies"

    name = fields.Char("Name")
    sh_type = fields.Many2one("sh.allergy.type", string="Allergy Type")
    sh_color = fields.Integer("Color", default=0)    
