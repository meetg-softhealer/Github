# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,_,Command #type:ignore
from odoo.exceptions import UserError, ValidationError #type:ignore
from datetime import datetime


class SaleOrder(models.Model):
    _inherit = "sale.order"

    sh_user_bool = fields.Boolean("", default=False)
    sh_group_bool = fields.Boolean("", default=False)    
    sh_show_bool = fields.Boolean(compute='_compute_sh_show_bool')

    sh_company_currency_id = fields.Many2one('res.currency', compute='_compute_company_currency_id')
    
    @api.depends_context('company')
    def _compute_company_currency_id(self):
        self.sh_company_currency_id = self.env.company.currency_id

    sh_total_amount = fields.Monetary(currency_field='sh_company_currency_id')
    
    def _compute_sh_show_bool(self):
        for record in self:            
            if self.state != 'sale':

                user_group = []

                for item in record.sh_group_ids:
                    for rec in item.users:
                        user_group.append(rec.id)

                record.sh_show_bool = self.env.user.id in user_group or self.env.user.id in record.sh_user_ids.ids
            else:
                record.sh_show_bool = False
        # print("\n\n compute called usrid \n\n", user_group)
    

    sh_approval_config_id = fields.Many2one("sh.approval.config", string="Approval Level", readonly=True)
    
    state = fields.Selection(string = 'Stage',selection_add = [('wait_approval', 'Waiting For Approval'),('sale',)])

    sh_next_approval_level = fields.Integer(string="Next Approval level", default=1, readonly=True)

    sh_user_ids = fields.Many2many("res.users", string="Users", readonly=True)

    sh_group_ids = fields.Many2many("res.groups", string="Groups", readonly=True)
    
    # @api.depends('sh_approval_config_id')
    # def _compute_sh_group_ids(self):
    #     for record in self:
    #         for rec in self.sh_approval_config_id.sh_approval_config_line_ids:
    #             if rec.sh_approver_type=='group':
    #                 for item in rec.sh_group_ids:
    #                     record.sh_group_ids = [(4,item.id)]

    sh_reject_date = fields.Datetime("Rejection Date", readonly=True)

    sh_rejected_by = fields.Many2one("res.users", string="Rejected By", readonly=True)

    sh_reject_reason = fields.Char("Rejection Reason", readonly=True)

    sh_so_approval_line_ids = fields.One2many("sh.so.approval.line", "sh_so_id", string="", readonly=True)
    
    # @api.model
    # def default_get(self, fields):
    #     res = super(SaleOrder, self).default_get(fields)   

    #     # current_id = self.env.context.get('active_id')
    #     # current_rec = self.env['sale.order'].browse(current_id)

    #     res['sh_user_id'] = self.env.user.id
    #     print("\n\n\n res", res)
    #     return res

    # def sh_bool_check(self):
    #     self.sh_user_bool2 = (self.env.user.id in self.sh_user_ids.ids)
    #     print("\n\n\n user bool 2", self.sh_user_bool2)

    #     user_group = []

    #     for item in self.sh_group_ids:
    #         for rec in item.users:
    #             user_group.append(rec.id)


    #     self.sh_group_bool2 = (self.env.user.id in user_group)
    #     print("\n\n\n group bool 2", self.sh_group_bool2)

    def sh_approve_action(self):

        item = self.sh_approval_config_id.sh_approval_config_line_ids

        print("\n\n\n next level", self.sh_next_approval_level)
        if len(self.sh_so_approval_line_ids) > 1: 
            if [(not self.sh_user_bool) and (item[self.sh_next_approval_level].sh_approver_type=='user')]:            
                self.sh_user_bool = True
                self.sh_user_ids = [(6,False,item[self.sh_next_approval_level].sh_user_ids.ids)]
               
                if self.sh_user_ids.ids:                        
                        for rec in self.sh_user_ids:
                            self.sh_approval_notifications(rec)
            
            if [(not self.sh_group_bool) and (item[self.sh_next_approval_level].sh_approver_type=='group')]:
                self.sh_group_bool = True
                self.sh_group_ids = [(6,False,item[self.sh_next_approval_level].sh_group_ids.ids)]
                
                if self.sh_group_ids:
                    for record in self.sh_group_ids:
                            for rec in record.users:
                                self.sh_approval_notifications(rec)

        for rec in self.sh_so_approval_line_ids:

            if len(self.sh_so_approval_line_ids)>self.sh_next_approval_level:
                if rec.sh_user_record_count:
                    self.sh_user_ids = [(6,False,item[self.sh_next_approval_level].sh_user_ids.ids)]
                   
                    if self.sh_user_ids.ids:                        
                        for recs in self.sh_user_ids:
                            self.sh_approval_notifications(recs)
            
                if rec.sh_group_record_count:                    
                    self.sh_group_ids = [(6,False,item[self.sh_next_approval_level].sh_group_ids.ids)]
                    
                    if self.sh_group_ids:
                        for record in self.sh_group_ids:
                            for recs in record.users:
                                self.sh_approval_notifications(recs)
            else:
                self.sh_user_ids = [(5,0,0)]
                self.sh_group_ids = [(5,0,0)]
            # print("\n\n\n user ids", self.sh_user_ids)
            if not rec.sh_status:
                rec.sh_status = True
                rec.sh_approved_date = datetime.now()
                rec.sh_approved_by = self.env.user.id

                if rec.sh_approval_level == len(self.sh_so_approval_line_ids):
                    self.sh_send_approval_email()
                    result = super(SaleOrder, self).action_confirm()
                    print("\n\n\n next approval level ", self.sh_next_approval_level)
                    return result        
        
                if self.sh_next_approval_level<len(self.sh_so_approval_line_ids)-1:
                    self.sh_next_approval_level += 1
                # else:
                #     self.sh_next_approval_level = len(self.sh_so_approval_line_ids)

                self.sh_send_approval_email()
                break
            
    def sh_reject_action(self):
        
        self.env['bus.bus']._sendone(                                   
                                    self.create_uid.partner_id,
                                     "simple_notification",
                                     {
                                        'type': 'info',
                                        'message': _(f"Dear salesperson your order {self.name} is rejected"),
                                     }
        )

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

        total = 0
        
        for rec in self.order_line:
            total += rec.price_subtotal
        
        self.sh_total_amount = total
        records = self.env['sh.approval.config'].search([('sh_min_amount','<=',total)])

        if records:
            difference = total - records[0].sh_min_amount
            record = records[0]
            for rec in records:            
                if total - rec.sh_min_amount < difference:
                    difference = total - rec.sh_min_amount
                    record = rec
            
            if self.env.company.id in record.sh_company_ids.ids:
                self.sh_approval_config_id = record.id

                count = 0
                for rec in self.sh_approval_config_id.sh_approval_config_line_ids:
                    count += 1
                    self.sh_so_approval_line_ids = [Command.create({
                        'sh_approval_level':count,
                        'sh_so_id':self.id,
                        'sh_status':False,
                        'sh_user_record_count':len(rec.sh_user_ids.ids),
                        'sh_group_record_count':len(rec.sh_group_ids.ids),
                    })]

                self.state = 'wait_approval'

                print("\n\n\n before")

                if self.sh_approval_config_id.sh_approval_config_line_ids[0].sh_approver_type == 'user':
                    self.sh_user_bool = True
                    self.sh_user_ids = [(6,False,self.sh_approval_config_id.sh_approval_config_line_ids[0].sh_user_ids.ids)]
                    
                    if self.sh_user_ids.ids:                        
                        for rec in self.sh_user_ids:
                            self.sh_approval_notifications(rec)

                # else:
                #     for rec in self.sh_approval_config_id.sh_approval_config_line_ids:
                #         if rec.sh_approver_type == 'user':
                            
                #             rec.sh_level
                #             self.sh_user_ids = [(6,False,rec.sh_user_ids.ids)]            
                #             break
                
                if self.sh_approval_config_id.sh_approval_config_line_ids[0].sh_approver_type == 'group':
                    self.sh_group_bool = True
                    self.sh_group_ids = [(6,False,self.sh_approval_config_id.sh_approval_config_line_ids[0].sh_group_ids.ids)]
                    
                    if self.sh_group_ids:
                        for record in self.sh_group_ids:
                            for rec in record.users:
                                self.sh_approval_notifications(rec)
                # else:
                #     for rec in self.sh_approval_config_id.sh_approval_config_line_ids:
                #         if rec.sh_approver_type == 'group':
                #             self.sh_group_ids = [(6,False,rec.sh_user_ids.ids)]            
                #             break
                # self.sh_bool_check()

                self.sh_send_approval_email()
                result = None

            else:            
                result = super(SaleOrder, self).action_confirm()

        else:            
            result = super(SaleOrder, self).action_confirm()

        return result

    def action_cancel(self):

        result = super(SaleOrder, self).action_cancel()

        for rec in self.sh_so_approval_line_ids:
            self.sh_so_approval_line_ids = [(2,rec.id)]

        return result

    def sh_approval_notifications(self, usr_id):        
        self.env['bus.bus']._sendone(                                   
                                    usr_id.partner_id,
                                     "simple_notification",
                                     {
                                        'type': 'info',
                                        'message': _(f"You have an approval notification for the sale order {self.name}"),
                                     }
        )

    def sh_send_approval_email(self):
        template = self.env.ref('sh_sale_dynamic_approval.sh_submit_for_approval_template')
        template.send_mail(self.id, force_send=True)

    def _confirmation_error_message(self):

        if self.state != 'wait_approval':

            result = super(SaleOrder, self)._confirmation_error_message()
            return result

        """ Return whether order can be confirmed or not if not then returm error message. """
        self.ensure_one()
        if self.state not in {'draft', 'sent', 'wait_approval'}:
            return _("Some orders are not in a state requiring confirmation.")
        if any(
            not line.display_type
            and not line.is_downpayment
            and not line.product_id
            for line in self.order_line
        ):
            return _("A line on these orders missing a product, you cannot confirm it.")

        return False

            
        