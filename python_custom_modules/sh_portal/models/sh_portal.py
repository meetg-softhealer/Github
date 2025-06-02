# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,_ #type:ignore
from odoo.exceptions import UserError #type:ignore

class ShPortal(models.Model):
    _name = "sh.portal"

    name = fields.Char("")

    sh_partner_id = fields.Many2one("res.partner", string="Partners")

    