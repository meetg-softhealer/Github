# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,_ #type:ignore
from odoo.exceptions import UserError, ValidationError #type:ignore


class ShResPartnerInherit(models.Model):
    _inherit = "res.partner"

    def _compute_display_name(self):               
        for rec in self:
            rec.display_name = f"{rec.env.company.name}, {rec.name}"