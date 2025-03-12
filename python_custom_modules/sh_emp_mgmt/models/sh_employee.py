# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api #type:ignore
from odoo.exceptions import UserError, ValidationError #type:ignore


class Employee(models.Model):
    _name = "sh.employee"

    name = fields.Char("Name")
    user_id = fields.Many2one("res.users", string="Manager")

    