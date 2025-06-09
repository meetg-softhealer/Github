# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,_,Command #type:ignore

class ShApprovalConfigLine(models.Model):
    _name = "sh.approval.config.line"

    name = fields.Char("")

    

    sh_approval_config_id = fields.Many2one("sh.approval.config")

    sh_level = fields.Integer(string="Level")
    
    # @api.onchange('sh_approval_config_id.sh_approval_config_line_ids')
    # def _onchange_(self):
    #     pass

    # @api.depends('sh_approval_config_id')
    # def _compute_sh_level(self):
    #     count = 0
    #     for record in self.sh_approval_config_id.sh_approval_config_line_ids:
    #         count += 1
    #         record.sh_level = count
    
    sh_approver_type = fields.Selection([('user','User'),('group','Group')], required=True, string="Appeove Process By")

    sh_user_ids = fields.Many2many("res.users", string="")
    sh_group_ids = fields.Many2many("res.groups", string="")

    # @api.onchange('sh_approver_type')
    # def _onchange_sh_approver_type(self):
        

    
    # @api.model
    # def create(self, values):
    
    
    #     result = super(ShApprovalConfigLine, self).create(values)
    #     count = 0
    #     for record in result['sh_approval_config_id'].sh_approval_config_line_ids:
    #         count += 1
    #         record.sh_level = count    

    #     return result
    