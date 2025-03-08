# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api #type:ignore
from odoo.exceptions import UserError, ValidationError #type:ignore

class sh_task(models.Model):
    _name = "sh.task"

    name = fields.Char("Name")
    amount = fields.Float("Amount")

    timesheet_id = fields.Many2one("sh.timesheet", string="Timesheet")