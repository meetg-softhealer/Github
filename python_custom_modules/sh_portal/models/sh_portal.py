# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,_ #type:ignore
from odoo.exceptions import UserError #type:ignore

class ShPortal(models.Model):
    _name = "sh.portal"
    _inherit = ["portal.mixin"]
    
    name = fields.Char("")

    sh_partner_id = fields.Many2one("res.partner", string="Partners")

    def _compute_access_url(self):
        super()._compute_access_url()
        for order in self:
            order.access_url = f'/my/sh_portal/{order.id}'
    