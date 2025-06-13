# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,_,Command #type:ignore
from odoo.exceptions import UserError, ValidationError #type:ignore
from datetime import datetime


class SaleOrder(models.Model):
    _inherit = "sale.order"

    sh_user_type_bool = fields.Boolean("", default=False, copy=False)
    sh_group_type_bool = fields.Boolean("", default=False, copy=False)    
    sh_show_button_bool = fields.Boolean(compute='_compute_sh_show_button_bool', copy=False)    
    sh_approval_config_id = fields.Many2one("sh.approval.config", string="Approval Level", readonly=True, copy=False)    
    state = fields.Selection(string = 'Stage',selection_add = [('wait_approval', 'Waiting For Approval'),('reject','Rejected'),('sale',)])
    sh_next_approval_level = fields.Integer(string="Next Approval level", default=0, readonly=True, copy=False)
    sh_user_ids = fields.Many2many("res.users", string="Users", readonly=True, copy=False)
    sh_group_ids = fields.Many2many("res.groups", string="Groups", readonly=True, copy=False)
    sh_reject_date = fields.Datetime("Rejection Date", readonly=True, copy=False)
    sh_rejected_by = fields.Many2one("res.users", string="Rejected By", readonly=True, copy=False)
    sh_reject_reason = fields.Char("Rejection Reason", readonly=True, copy=False)
    sh_so_approval_line_ids = fields.One2many("sh.so.approval.line", "sh_so_id", string="", readonly=True, copy=False)
    sh_partner_ids = fields.Many2many("res.partner", copy=False)

    def _compute_sh_show_button_bool(self):
        for record in self:            
            if self.state != 'sale' and self.state != 'cancel':

                user_group = self.sh_group_ids.mapped('users').ids
                record.sh_show_button_bool = self.env.user.id in user_group or self.env.user.id in record.sh_user_ids.ids
            else:
                record.sh_show_button_bool = False        


    def sh_approve_action(self):

        item = self.sh_approval_config_id.sh_approval_config_line_ids
        
        if len(self.sh_so_approval_line_ids) > 1 and self.sh_next_approval_level < len(self.sh_so_approval_line_ids): 
            if [(not self.sh_user_type_bool) and (item[self.sh_next_approval_level].sh_approver_type=='user')]:            
                
                self.sh_user_type_bool = True
                self.sh_user_ids = [(6,False,item[self.sh_next_approval_level].sh_user_ids.ids)]
                if self.sh_user_ids:
                        self.sh_partner_ids = self.sh_user_ids.mapped('partner_id')                
            
            if [(not self.sh_group_type_bool) and (item[self.sh_next_approval_level].sh_approver_type=='group')]:
                
                self.sh_group_type_bool = True
                self.sh_group_ids = [(6,False,item[self.sh_next_approval_level].sh_group_ids.ids)]                
                

                if self.sh_group_ids:
                    usr_list = self.sh_group_ids.mapped('users').mapped('partner_id').ids           
                    self.sh_partner_ids = [(6,False,usr_list)]
                

        for rec in self.sh_so_approval_line_ids:

            if len(self.sh_so_approval_line_ids)>self.sh_next_approval_level:
                if rec.sh_user_record_count_ids:
                
                    self.sh_user_ids = [(6,False,item[self.sh_next_approval_level].sh_user_ids.ids)]
                    if self.sh_user_ids:
                        self.sh_partner_ids = self.sh_user_ids.mapped('partner_id')                    

                if rec.sh_group_record_count_ids:  
                
                    self.sh_group_ids = [(6,False,item[self.sh_next_approval_level].sh_group_ids.ids)]                    
                    
                    if self.sh_group_ids:
                        usr_list = self.sh_group_ids.mapped('users').mapped('partner_id').ids            
                        self.sh_partner_ids = [(6,False,usr_list)]
                

            elif len(self.sh_so_approval_line_ids)==self.sh_next_approval_level:
                if rec.sh_user_record_count_ids:
                
                    self.sh_user_ids = [(6,False,item[self.sh_next_approval_level-1].sh_user_ids.ids)]
                    if self.sh_user_ids:
                        self.sh_partner_ids = self.sh_user_ids.mapped('partner_id')                

                if rec.sh_group_record_count_ids:  
                
                    self.sh_group_ids = [(6,False,item[self.sh_next_approval_level-1].sh_group_ids.ids)]
                    

                    if self.sh_group_ids:
                        usr_list = self.sh_group_ids.mapped('users').mapped('partner_id').ids
                        self.sh_partner_ids = [(6,False,usr_list)]
                

            else:
                self.write({'sh_user_ids':[(Command.clear())],
                            'sh_group_ids':[(Command.clear())]
                            })

            if not rec.sh_status:
                rec.sh_status = True
                rec.sh_approved_date = datetime.now()
                rec.sh_approved_by = self.env.user.id

                if rec.sh_approval_level == len(self.sh_so_approval_line_ids):  
                    self.sh_confirmation_notification(self.create_uid)
                    self.sh_order_confirm_email()                  
                    result = super(SaleOrder, self).action_confirm()                    
                    return result        
        
                if self.sh_next_approval_level<=len(self.sh_so_approval_line_ids)-1:
                    self.sh_next_approval_level += 1

                for people in self.sh_partner_ids:
                    self.sh_approval_notifications(people)
                    
                self.sh_send_approval_email()
                break
            
    def sh_reject_action(self):

        return {
            'type': 'ir.actions.act_window',
            'name': _('Rejection Reason'),  
            'res_model': 'sh.reject.action.wizard',
            'view_mode': 'form',
            'target': 'new',
            'view_id':self.env.ref('sh_sale_dynamic_approval.sh_reject_action_wizard_view_form').id,            
            'context':{'default_sh_so_id':self.id,
                       }
        }

    def action_confirm(self):

        record = self.env['sh.approval.config'].search([('sh_min_amount','<=',self.amount_untaxed),('sh_company_id','=',self.env.company.id)], order='sh_min_amount desc', limit=1)    
    
        if record:            
            self.sh_next_approval_level = 1
            self.sh_approval_config_id = record.id

            count = 0
            for rec in self.sh_approval_config_id.sh_approval_config_line_ids:
                count += 1
                self.sh_so_approval_line_ids = [Command.create({
                    'sh_approval_level':count,
                    'sh_so_id':self.id,
                    'sh_status':False,
                    'sh_user_record_count_ids':rec.sh_user_ids.ids,
                    'sh_group_record_count_ids':rec.sh_group_ids.ids,
                })]

            self.state = 'wait_approval'                

            if self.sh_approval_config_id.sh_approval_config_line_ids[0].sh_approver_type == 'user':
            
                self.sh_user_type_bool = True
                self.sh_user_ids = [(6,False,self.sh_approval_config_id.sh_approval_config_line_ids[0].sh_user_ids.ids)]
                if self.sh_user_ids:
                    self.sh_partner_ids = self.sh_user_ids.mapped('partner_id')                    

            if self.sh_approval_config_id.sh_approval_config_line_ids[0].sh_approver_type == 'group':
            
                self.sh_group_type_bool = True
                self.sh_group_ids = [(6,False,self.sh_approval_config_id.sh_approval_config_line_ids[0].sh_group_ids.ids)]
                
                if self.sh_group_ids:
                    usr_list = self.sh_group_ids.mapped('users').mapped('partner_id').ids
                    self.sh_partner_ids = [(6,False,usr_list)]      
            
            for people in self.sh_partner_ids:
                self.sh_approval_notifications(people)

            self.sh_send_approval_email()
            result = None

        else:            
            result = super(SaleOrder, self).action_confirm()

        return result

    def action_cancel(self):

        result = super(SaleOrder, self).action_cancel()

        for rec in self.sh_so_approval_line_ids:
            self.sh_so_approval_line_ids = [(2,rec.id)]

        return result

    def sh_approval_notifications(self, partner_id):        
        self.env['bus.bus']._sendone(                                   
                                    partner_id,
                                     "simple_notification",
                                     {
                                        'type': 'info',
                                        'message': _(f"You have an approval notification for the sale order {self.name}"),
                                     }
        )

    def sh_confirmation_notification(self, usr_id):        
        self.env['bus.bus']._sendone(                                   
                                    usr_id.partner_id,
                                     "simple_notification",
                                     {
                                        'type': 'info',
                                        'message': _(f"Your sale order {self.name} is approved and has been confirmed!!!"),
                                     }
        )

    def sh_send_approval_email(self):
        template = self.env.ref('sh_sale_dynamic_approval.sh_submit_for_approval_template')
        template.send_mail(self.id, force_send=True)

    def sh_send_rejection_email(self):
        template = self.env.ref('sh_sale_dynamic_approval.sh_reject_approval_template')
        template.send_mail(self.id, force_send=True)

    def sh_order_confirm_email(self):
        template = self.env.ref('sh_sale_dynamic_approval.sh_order_confirm_template')
        template.send_mail(self.id, force_send=True)

    def action_draft(self):
        if self.state == 'reject':

            self.sh_reject_date = False
            self.sh_rejected_by = False
            self.sh_reject_reason = False
            self.sh_so_approval_line_ids:False
                        
            return super(SaleOrder, self).action_draft()

    def _confirmation_error_message(self):

        self.ensure_one()
        if self.state in {'draft', 'sent', 'wait_approval'}:
            return False
            
        return super(SaleOrder, self)._confirmation_error_message()
        

            
        