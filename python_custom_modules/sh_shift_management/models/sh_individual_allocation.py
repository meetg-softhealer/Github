# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,_,Command #type:ignore
from datetime import datetime
from datetime import timedelta

class ShChangeShiftRequest(models.Model):
    _name = "sh.individual.allocation"
    _inherit = "sh.shift.allocation"

    sh_employee_id = fields.Many2one("hr.employee", string="Employee")

    sh_change_shift_stage = fields.Selection([('draft','Draft'),
                                              ('wait','Waiting For Approval'),
                                              ('approve','Approved'),
                                              ('reject','rejected')
                                              ], default='draft')                                            
    
    def sh_update_allocation_request_action(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Update Allocation Wizard'),   #type:ignore
            'res_model': 'sh.update.allocation.wizard',
            'target': 'new',
            'view_mode': 'form',
            'view_id':self.env.ref('sh_shift_management.sh_update_allocation_wizard_view_form').id,            
            'context':{'default_sh_allocation_id':self.id}             
        }

    def sh_approve_request_action(self):
        pass

    def sh_reject_request_action(self):
        pass