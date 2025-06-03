# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,_ #type:ignore
from odoo.exceptions import UserError, ValidationError #type:ignore


class ShMassUpdate(models.Model):
    _name = "sh.mass.update"

    name = fields.Char("")

    sh_model_ids = fields.Many2many("ir.model", string="Models")
