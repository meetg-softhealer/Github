# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models #type:ignore


class ShResourceCalendarAttendence(models.Model):
    _name = "sh.scheduled.info"

    sh_shift_allocation_id = fields.Many2one("sh.shift.allocation")

    sh_date = fields.Date("Date")
    sh_shift_type_id = fields.Many2one("sh.shift.type", string="Shift Type")
    sh_dayofweek = fields.Selection([('Sunday','Sunday'),
                                     ('Monday','Monday'),
                                     ('Tuesday','Tuesday'),
                                     ('Wednesday','Wednesday'),
                                     ('Thursday','Thursday'),
                                     ('Friday','Friday'),
                                     ('Saturday','Saturday')
                                     ], string="Day")