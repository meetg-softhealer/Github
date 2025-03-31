# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,_ #type:ignore
from odoo.exceptions import UserError #type:ignore

class sh_temp_table(models.Model):
    _name = 'temp.table'

    name = fields.Char(string="Name")
    tech_name = fields.Char(string='Tech Name')