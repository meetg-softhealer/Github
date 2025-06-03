# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,_ #type:ignore
from odoo.exceptions import UserError, ValidationError #type:ignore


class IrModel(models.Model):
    _inherit = "ir.model"

    sh_bool = fields.Boolean("")