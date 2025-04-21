# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,_ #type:ignore 
from odoo.exceptions import UserError #type:ignore

class ShAllergies(models.Model):
    _name = "sh.allergy.type"

    name = fields.Char("Name")

