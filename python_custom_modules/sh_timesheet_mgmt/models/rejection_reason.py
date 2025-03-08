from odoo import models,fields,api #type:ignore
from odoo.exceptions import UserError, ValidationError #type:ignore

class rejection_reason(models.TransientModel):
    _name = "sh.rejection.reason"

    name = fields.Char("Rejection Reason")
    # timesheet_id = fields.Many2one("sh.timesheet", string="Timesheet")
    
    def save_wizard_action(self):
        # print("\n\n\n\n\n=======",self.env.context)
        current_id = self.env.context.get('active_id')
        # print(current_id.state)
        current_record = self.env['sh.timesheet'].browse(current_id)
        current_record.state = 'rejected'

        current_record.reject_reason = self.name


# access_account_lock_exception,account.lock_exception,model_account_lock_exception,base.group_user,1,0,0,0
# access_account_lock_exception_manager,account.lock_exception manager,model_account_lock_exception,account.group_account_manager,1,0,1,0