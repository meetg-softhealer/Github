# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,_ #type:ignore 
from odoo.exceptions import UserError #type:ignore

class ShIngredients(models.Model):
    _name = "sh.ingredients"

    name = fields.Char("Ingredient Name")
    sh_color = fields.Integer("Color")
    