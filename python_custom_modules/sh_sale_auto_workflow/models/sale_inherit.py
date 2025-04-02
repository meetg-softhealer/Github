# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,_ #type:ignore
from odoo.exceptions import UserError #type:ignore

class sale_order_inherit(models.Model):
    _inherit = "sale.order"

    sale_workflow_id = fields.Many2one("sh.sale.auto.workflow", string="Sale Workflow", 
    default=lambda self: self.env.company.bydefault_workflow)
    
    company_id = fields.Many2one("res.company")

    def action_confirm(self):
        rtn = super(sale_order_inherit, self).action_confirm()

        if self.company_id.enable_auto_workflow:
            print("\n\n\n\n====== called auto start")
            self.auto_start()

        return rtn

    def auto_start(self):
        
        print("\n\n\n\n\n\n\n=========== in autostart")
        obj = self.sale_workflow_id
        
        if obj.delivery_order:
            print("\n\n\n\n\n\n\n=========== in delivery order")
            self.env['stock.picking'].search([('origin','=',self.name)]).button_validate()
            
        if obj.create_invoice:
            print("\n\n\n\n\n\n\n=========== in create")
            inv = self._create_invoices()

            if obj.validate_invoice:
                inv.action_post()

                if obj.register_payment:
                    print("\n\n\n\n\n\n\n=========== in register payment",self.env['account.payment.register'])
                    
                    self.env['account.payment.register'].with_context(
                        active_model = "account.move",
                        active_ids = inv.ids,
                        payment_method_line_id = self.sale_workflow_id.payment_journal.id,
                        journal_id = self.sale_workflow_id.sale_journal.id
                    ).create({"group_payment": False}).action_create_payments()

                if obj.invoice_by_mail:
                    self.env['account.move.send.wizard'].with_context(
                        active_model = "account.move",
                        active_id = self.id,
                        mail_partner_ids = self.partner_id.id
                    ).create({'move_id':inv.id}).action_send_and_print()

            

            