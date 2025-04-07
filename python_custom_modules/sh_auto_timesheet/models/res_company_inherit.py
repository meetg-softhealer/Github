# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models #type:ignore


class ResCompany(models.Model):
    _inherit = "res.company"

    group_enable_bool = fields.Boolean()