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

        self.env['bus.bus']._sendone(                                   
                                    self.sh_so_id.create_uid.partner_id,
                                     "simple_notification",
                                     {
                                        'type': 'info',
                                        'message': _(f"Dear salesperson your order {self.sh_so_id.name} is rejected"),
                                     }
        )

        self.sh_so_id.sh_send_rejection_email()
        self.sh_so_id.sh_next_approval_level = 1
        self.sh_so_id.sh_user_ids = [(5,0,0)]
        self.sh_so_id.sh_group_ids = [(5,0,0)]

        result = self.sh_so_id.action_cancel()
        return result
        