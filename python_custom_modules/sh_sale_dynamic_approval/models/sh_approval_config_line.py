# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,_,Command #type:ignore
from odoo.exceptions import UserError #type:ignore

class ShApprovalConfigLine(models.Model):
    _name = "sh.approval.config.line"

    sh_company_id = fields.Many2one("res.company", default=lambda self:self.env.company.id)
    sh_approval_config_id = fields.Many2one("sh.approval.config")
    sh_level = fields.Integer(string="Level", required=True)    
    sh_approver_type = fields.Selection([('user','User'),('group','Group')], required=True, string="Appeove Process By")
    sh_user_ids = fields.Many2many("res.users", string="")
    sh_group_ids = fields.Many2many("res.groups", string="")
    