# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,_ #type:ignore


class sh_support_ticket(models.TransientModel):
    _name = "support.ticket.wizard"

    # Field to allow users to change the status of multiple tickets at once
    status = fields.Selection([("new","New"),("progress","In Progress"),("resolved","Resolved"),("closed","Closed")], default='new', string="Status")

    # Mass action method to update the status of selected support tickets
    def mass_close_tickets_wizard(self):            
        
        active_ids = self.env.context.get('active_ids', []) # Get selected ticket IDs from context
        if active_ids:
            tickets = self.env['support.ticket'].browse(active_ids) # Fetch ticket records
            tickets.write({'status': self.status}) # Update status of selected tickets