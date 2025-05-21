# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models #type:ignore


class ShDays(models.Model):
    _name = "sh.days"

    name = fields.Char("Name")