# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,_ #type:ignore 
from odoo.exceptions import UserError #type:ignore

class ShSpecialization(models.Model):
    _name = "sh.specialization"

    name = fields.Char("Name")
    sh_description = fields.Text("Description")
    