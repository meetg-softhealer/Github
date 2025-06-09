# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,_ #type:ignore
from odoo.exceptions import UserError #type:ignore
from datetime import datetime

class ShRejectActionWizard(models.TransientModel):
    _name = "sh.reject.action.wizard"

    sh_so_id = fields.Many2one("sale.order") 
    sh_reason = fields.Char("Rejection Reason", required=True)
    
    def confirm_action(self):

        self.sh_so_id.sh_reject_reason = self.sh_reason
        self.sh_so_id.sh_reject_date = datetime.now()
        self.sh_so_id.sh_rejected_by = self.env.user.id

        result = self.sh_so_id.action_cancel()
        return result
        