# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api #type:ignore
from odoo.exceptions import UserError, ValidationError #type:ignore


class design_category(models.Model):
    _name = "sh.design.category"

    name = fields.Char("Name")