# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,_ #type:ignore
from odoo.exceptions import UserError #type:ignore

class sale_order_inherit(models.Model):
    _inherit = "sale.order"

    sale_workflow = fields.Many2one("sh.sale.auto.workflow", string="Sale Workflow")

    def action_confirm(self):
        print("\n\n\n\n\n\n\n\n======inherited action")

        for order in self:
            error_msg = order._confirmation_error_message()
            if error_msg:
                raise UserError(error_msg)

        self.order_line._validate_analytic_distribution()

        for order in self:
            if order.partner_id in order.message_partner_ids:
                continue
            order.message_subscribe([order.partner_id.id])

        self.write(self._prepare_confirmation_values())

        # Context key 'default_name' is sometimes propagated up to here.
        # We don't need it and it creates issues in the creation of linked records.
        context = self._context.copy()
        context.pop('default_name', None)

        self.with_context(context)._action_confirm()
        user = self[:1].create_uid
        if user and user.sudo().has_group('sale.group_auto_done_setting'):
            # Public user can confirm SO, so we check the group on any record creator.
            self.action_lock()

        if self.env.context.get('send_email'):
            self._send_order_confirmation_mail()


        self.auto_start()

        return True
    
    def auto_start(self):
        
        print("\n\n\n\n\n\n\n===========autostart")

        if self.sale_workflow.delivery_order:
            def button_validate(self):
                super().button_validate()
            
            self.env['stock.picking'].search[('origin','=',self.name)].button_validate()