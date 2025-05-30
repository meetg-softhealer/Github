# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,_,Command #type:ignore
from odoo.exceptions import UserError #type:ignore


class ShUpdateAllocationWizard(models.TransientModel):
    _name = "sh.update.allocation.wizard"
    sh_allocation_id = fields.Many2one("sh.change.shift.request")

    sh_employee_id = fields.Many2one("hr.employee", string="Employee")
    sh_employee_ids = fields.Many2many("hr.employee", string="Employee")
    sh_resource_calendar_id = fields.Many2one("resource.calendar", string="Shift Schedule")
    sh_shift_type = fields.Many2one("sh.shift.type", string="Shift Type")
    sh_from_date = fields.Datetime("From Date")
    sh_to_date = fields.Datetime("To Date")
    sh_working_hours = fields.Float("Working Hours")

    def wizard_create_action(self):
        print("allocationid \n\n\n", self.sh_allocation_id)
        self.sh_allocation_id.sh_change_request_line_ids = [Command.create({
            'name':self.sh_allocation_id.name,
            'sh_allocation_id':self.sh_allocation_id.id,
            'sh_employee_id':self.sh_employee_id.id,
            'sh_resource_calendar_id':self.sh_resource_calendar_id.id,
            'sh_shift_type':self.sh_shift_type.id,
            'sh_from_date':self.sh_from_date,
            'sh_to_date':self.sh_to_date,
            'sh_working_hours':self.sh_working_hours
        })]



