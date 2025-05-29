# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models #type:ignore


class ResCompany(models.Model):
    _inherit = "res.company"

    # sh_enable_custom_shift = fields.Boolean("Enable Custom Shift Configuration")
    # sh_restrict_checkout = fields.Boolean("Restrict heckout if working hours are not completed!!!")
    sh_notify_shift = fields.Boolean("Notify Shift Allocation Before")
    sh_days = fields.Integer("Days")


