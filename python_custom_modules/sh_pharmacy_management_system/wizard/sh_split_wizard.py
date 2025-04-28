# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,Command,_ #type:ignore
from odoo.exceptions import UserError #type:ignore

class ShSplitWizard(models.TransientModel):
    _name = "sh.split.wizard"

    sh_order_id = fields.Many2one("sale.order")
    sh_order_line_ids = fields.Many2many("sh.split.wizard.line",string="Products")
    sh_partner_id = fields.Many2one("res.partner", string="Customer")

    @api.model
    def default_get(self, fields):

        res = super(ShSplitWizard, self).default_get(fields)
        
        current_id = self.env.context.get('active_id')
        current_rec = self.env['sale.order'].browse(current_id)
        
        res['sh_partner_id'] = current_rec.partner_id.id
        # res['sh_order_line_ids'] = [(0,0,{'sh_name':rec.name,
        #                                   'sh_sol_lot_no':rec.sh_lot_no,
        #                                    'sh_sol_expiry_date':rec.sh_expiry_date,
        #                                    'sh_product_template_id':rec.product_template_id.id,
        #                                    'sh_product_product_id':rec.product_id.id,
        #                                    'sh_product_uom_qty':rec.product_uom_qty}) for rec in current_rec.order_line if rec['select_bool']]  

        res['sh_order_line_ids'] = [Command.create({
                                           'sh_order_line_id':rec.id,
                                           'sh_name':rec.name,
                                           'sh_sol_lot_no':rec.sh_lot_no,
                                           'sh_sol_expiry_date':rec.sh_expiry_date,
                                        #    'sh_product_template_id':rec.product_template_id.id,
                                           'sh_product_product_id':rec.product_id.id,
                                           'sh_product_uom_qty':rec.product_uom_qty}) for rec in current_rec.order_line if rec['select_bool']]
        print("\n\n\n for sh_order_line_id", res)
        return res

    def sh_wizard_confirm_action(self):
        
        self.env['sale.order'].create({
            'partner_id':self.sh_partner_id.id,
            'order_line':[(0,0,{'name':line.sh_name,
                                'sh_lot_no':line.sh_sol_lot_no,
                                'sh_expiry_date':line.sh_sol_expiry_date,
                                # 'product_id':line.sh_product_template_id.product_variant_id.id,
                                'product_id':line.sh_product_product_id.id,
                                'product_uom_qty':line.sh_product_uom_qty}) for line in self.sh_order_line_ids]
        })
        
        sol_ids = self.env['sale.order.line'].search([('order_id','=',self.sh_order_id.id)])

        for rec in self.sh_order_line_ids:
            fil_rec = sol_ids.filtered(lambda x:x.id == rec.sh_order_line_id.id)
            print("\n\n\n fil_rec", fil_rec)
            if rec.sh_order_line_id.id in sol_ids.ids:
                print('\n\n\nrec.sh_order_line_id',rec.sh_order_line_id)
                fil_rec.product_uom_qty -= rec.sh_product_uom_qty
      
        self.sh_wizard_cancel_action()
        
    def sh_wizard_cancel_action(self):
        self.sh_order_id.order_line.select_bool = False




        

