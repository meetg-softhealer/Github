# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api #type:ignore
from odoo.exceptions import UserError, ValidationError #type:ignore


class design_type(models.Model):
    _name = "sh.design.type"

    name = fields.Char("Name")
    img = fields.Image()