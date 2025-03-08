# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api #type:ignore
from odoo.exceptions import UserError, ValidationError #type:ignore

class sh_tag(models.Model):
    _name = "sh.tag"

    name = fields.Char("Name")