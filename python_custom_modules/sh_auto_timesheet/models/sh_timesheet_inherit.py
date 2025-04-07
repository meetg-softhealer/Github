# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,_ #type:ignore
from odoo.exceptions import UserError, ValidationError #type:ignore


class sh_timesheet_inherit(models.Model):
    _inherit = "account.analytic.line"

    calendar_id = fields.Many2one("calendar.event")