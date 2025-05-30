# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,_,Command #type:ignore
from datetime import datetime
from datetime import timedelta

class ShChangeShiftRequest(models.Model):
    _name = "sh.change.shift.request"
    # _inherit = "sh.shift.allocation"

    name = fields.Char(related='sh_shift_allocation_id.name')

    sh_shift_allocation_id = fields.Many2one("sh.shift.allocation")
    sh_bool = fields.Boolean(related='sh_shift_allocation_id.sh_bool')

    sh_resource_calendar_id = fields.Many2one("resource.calendar", string="Shift Schedule", required=True, related='sh_shift_allocation_id.sh_resource_calendar_id')
    sh_employee_ids = fields.Many2many("hr.employee", string="Employees", required=True, related='sh_shift_allocation_id.sh_employee_ids')   
    sh_shift_type_id = fields.Many2one("sh.shift.type", string="Shift Type", required=True, related='sh_shift_allocation_id.sh_shift_type_id')

    sh_from_date = fields.Datetime("From Date", required=True, related='sh_shift_allocation_id.sh_from_date')
    sh_to_date = fields.Datetime("To Date", required=True, related='sh_shift_allocation_id.sh_to_date')
    sh_working_hours = fields.Float("Working Hours", related='sh_resource_calendar_id.hours_per_day')

    sh_scheduled_info_ids = fields.One2many("sh.scheduled.info", "sh_shift_allocation_id", related='sh_shift_allocation_id.sh_scheduled_info_ids')

    sh_change_request_line_ids = fields.Many2many("sh.change.request.line",
                                                  "sh_change_shift_request_sh_change_shift_request_line_rel",
                                                  "sh_change_shift_request_id"
                                                  "sh_shift_req_line_id",
                                                   string="Change Requests")

    def sh_update_allocation_request_action(self):
        print("sh_change_request_line_ids", self.env['sh.change.request.line'].search([]))
        return {
            'type': 'ir.actions.act_window',
            'name': _('Update Allocation Wizard'),   #type:ignore
            'res_model': 'sh.update.allocation.wizard',
            'target': 'new',
            'view_mode': 'form',
            'view_id':self.env.ref('sh_shift_management.sh_update_allocation_wizard_view_form').id,            
            'context':{'default_sh_allocation_id':self.id,
                       'default_sh_employee_ids':self.sh_employee_ids.ids}             
        }

    