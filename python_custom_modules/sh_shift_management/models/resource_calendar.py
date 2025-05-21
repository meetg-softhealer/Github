# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models #type:ignore


class ShResourceCalendar(models.Model):
    _inherit = "resource.calendar"

    sh_shift_type = fields.Many2one("sh.shift.type", string="Shift Type")
    sh_shift_manager = fields.Many2one("res.users", string="Shift Manager")
    sh_active = fields.Boolean("Active")

    sh_days_ids = fields.Many2many("sh.days", string="Week-off Days")
    