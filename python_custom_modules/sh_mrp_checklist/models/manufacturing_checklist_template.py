# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,_ #type:ignore
from odoo.exceptions import UserError #type:ignore

class ManufacturingChecklistTemplate(models.Model):
    _name = "manufacturing.checklist.template"

    name = fields.Char("Name", required=True)
    company_id = fields.Many2one("res.company", string="Company", required=True)

    check_list_ids = fields.Many2many("manufacturing.checklist",string="Check List")
    