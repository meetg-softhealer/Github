# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,_ #type:ignore
from odoo.exceptions import UserError #type:ignore
from datetime import datetime
from dateutil.relativedelta import relativedelta
import logging


_logger = logging.getLogger(__name__)

class sh_support_ticket(models.Model):
    _name = "support.ticket"
    _inherit = ['mail.thread.cc',
                'mail.activity.mixin',
                'utm.mixin',
                'mail.tracking.duration.mixin',
            ]

    name = fields.Char(default="New")
    customer_id = fields.Many2one("res.partner", string="Customer")
    priority = fields.Selection([("low","Low"),("medium","Medium"),("high","High")])
    developer_id= fields.Many2one("res.users", string="Developers")
    status = fields.Selection([("new","New"),("progress","In Progress"),("resolved","Resolved"),("closed","Closed")], default='new')
    creation_date = fields.Date(compute='_compute_creation_date', string="Creation Date")
    resolved_date = fields.Date(string="Issue Resolved Date")
    invoice_ids = fields.One2many("account.move", "ticket_id", string="Invoices")

    # Compute the creation date as today's 
    def _compute_creation_date(self):
        for record in self:
            record.creation_date = datetime.today()

    # support_leader = fields.Many2one("res.users", string="Support Leader")
    # sl_rating = fields.Selection([('one','1'),('two','2'),('three','3'),('four','4'),('five','5')], compute='_compute_sl_rating', string="Sl Rating")
        
    # Compute rating from the assigned support leader
    # @api.depends('support_leader')
    # def _compute_sl_rating(self):
    #     for record in self:
    #         record.sl_rating = record.support_leader.rating
            
    # Update resolved date when status changes to resolved
    @api.onchange('status')
    def _onchange_status(self):
        if self.status == "resolved":
            self.resolved_date = datetime.today()

    # Automatically close tickets that have been resolved for more than 7 days
    def _cron_resolved(self):
        resolved_ids =  self.env['support.ticket'].search([('resolved_date','<=',datetime.today()-relativedelta(days=7))])       
        for record in resolved_ids:
            record.status = 'closed'

    # Smart button action to open related invoices
    def invoice_smart_button_action(self):
        return {
            'name': _('Invoice'), 
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'list,form',
            'domain': [('partner_id', 'in', [self.customer_id.id])] #for list view
        }

    # Override create method to generate sequence for ticket name
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _("New")) == _("New"): 
                seq_date = fields.Datetime.context_timestamp(
                    self, fields.Datetime.to_datetime(vals['creation_date'])
                ) if 'creation_date' in vals else None
                vals['name'] = self.env['ir.sequence'].with_company(vals.get('company_id')).next_by_code(
                    'support.ticket', sequence_date=seq_date) or _("New")   

        return super().create(vals_list)
    
    # Override write method to log status change
    def write(self, vals):
        if vals.get('status'):
            _logger.info(f"The status has benn changed to {vals['status']} !!!")

        return super(sh_support_ticket, self).write(vals)
    
    # Change status to In Progress
    def status_to_progress(self):
        print("\n\n\n\n\n=========")
        self.status = 'progress'
        print("\n\n\n\n\n======",self.status)

    # Change status to Resolved
    def status_to_resolved(self):
        self.status = 'resolved'

    # Change status to Closed
    def status_to_closed(self):
        for ticket in self:
            ticket.status = 'closed'

            self.env['account.move'].create({
                'partner_id' : self.customer_id.id,
                'invoice_date': datetime.today(),
                'ticket_id': ticket.id,
                'move_type':'out_invoice',
                'invoice_line_ids': [(0,0,{
                    'name': ticket.name,
                    'quantity':'1',
                    'price_unit':'10'}
                )]  
            })


    # Open a wizard to close the ticket
    def close_ticket(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Close Ticket'),   #type:ignore
            'res_model': 'support.ticket.wizard',
            'target': 'new',
            'view_mode': 'form',
            'context' : {'hi':'hi'}
        }

    # Set default priority for new tickets
    @api.model
    def default_get(self, fields):
        res = super(sh_support_ticket, self).default_get(fields)           
        res.update({'priority':'low'})
        return res
    
    # Ensure a developer is assigned to only one active ticket at a time
    @api.constrains('developer_id')
    def unique_developer(self):
        tickets = self.search([('developer_id', "=", self.developer_id.id),('id','!=',self.id)])
        for record in tickets:
            if record.status != 'closed':                              #record.status == 'progress' or record.status == 'new':
                raise UserError("The developer has been already assigned with a task !!!")

            
class res_user_inherit(models.Model):
    _inherit = "res.users"

    is_support_lead = fields.Boolean(string="Is a SL?")
    rating = fields.Selection([('one','1'),('two','2'),('three','3'),('four','4'),('five','5')], string="Rating")

class res_partner_inherit(models.Model):

    _inherit = "res.partner"

    # Smart button action to open related support tickets
    def ticket_smart_button_action(self):

        return {
            'type': 'ir.actions.act_window',
            'name': _('Support Ticket'),  
            'res_model': 'support.ticket',
            'view_mode': 'list,form',
            'domain': [('customer_id', '=',self.id)],
        }
    
class account_move_inherit(models.Model):

    _inherit = "account.move"

    ticket_id = fields.Many2one("support.ticket", string="Ticket")

    