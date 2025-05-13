# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,Command,_ #type:ignore
from odoo.exceptions import UserError #type:ignore

class ShSaleOrderInherit(models.Model):
    _inherit = "sale.order"

    sh_gender = fields.Selection(selection=[('male','Male'),('female','Female')],string="Gender", tracking=True)
    sh_age = fields.Integer(string="Age", tracking=True, readonly=True, related='partner_id.sh_age')
    
    sh_doctor_id = fields.Many2one("res.partner", string="Doctor", domain=[(('sh_is_doctor','=', True))], tracking=True)

    sh_precription = fields.Binary(string='Prescription', tracking=True)

    sh_mobile_number = fields.Char("Mobile Number")

    sh_card = fields.Char(string="Aadhar Card",size=12,tracking=True)

    sh_email = fields.Char("Email")

    sh_is_narcotic = fields.Boolean()

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        self.sh_gender = self.partner_id.sh_gender
        # self.sh_age = self.partner_id.sh_age
        self.sh_mobile_number = self.partner_id.mobile
        self.sh_card = self.partner_id.sh_card
        self.sh_email = self.partner_id.email

    @api.onchange('order_line')
    def _onchange_order_line(self):
        for rec in self.order_line:
            if rec.product_id.categ_id.sh_is_narcotic:
                self.sh_is_narcotic = True
    
    def sh_split_action(self):
        print("\n\n\n Split called \n\n\n")
        return {
            'type': 'ir.actions.act_window',
            'name': _('Split Order'),   #type:ignore
            'res_model': 'sh.split.wizard',
            'target': 'new',
            'view_mode': 'form',
            'view_id':self.env.ref('sh_pharmacy_management_system.sh_split_wizard_view_form').id,            
            'context':{'default_sh_order_id':self.id} #'default_sh_order_line_ids':self.order_line.filtered(lambda rec: rec.select_bool == True).ids}
            # 'next': {'type': 'ir.actions.act_window_close'}                        
        }
    
    def sh_calculate_commission(self):
        if self.sh_doctor_id.sh_commission_types=='fixed':  
            return self.sh_doctor_id.sh_amount
        elif self.sh_doctor_id.sh_commission_types=='percent':
            return (self.amount_untaxed*self.sh_doctor_id.sh_commission_percent)/100

    def action_confirm(self):
        result = super(ShSaleOrderInherit, self).action_confirm()
        print("\n\n self.sh_doctor_id", self.sh_doctor_id.sh_commission_types)
        if self.sh_doctor_id and self.sh_doctor_id.sh_commission_types!='none':
            self.env['sh.doctor.commission'].create({
                'sh_res_partner_id':self.sh_doctor_id.id,
                'sh_date':self.date_order,
                'sh_so_id':self.id,
                'sh_so_id_patient_name':self.partner_id.id,
                'sh_so_amount':self.amount_untaxed,
                'sh_commission_types':self.sh_doctor_id.sh_commission_types,
                'sh_total_commission':self.sh_calculate_commission()
            })
            self.sh_doctor_id.sh_create_commission_line()
                   
        return result
    
    

    

