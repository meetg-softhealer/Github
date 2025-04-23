# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,_ #type:ignore
from odoo.exceptions import UserError #type:ignore

class ShSaleOrderInherit(models.Model):
    _inherit = "sale.order"

    sh_gender = fields.Selection(selection=[('male','Male'),('female','Female')],string="Gender", tracking=True)
    sh_age = fields.Integer(string="Age", tracking=True)

    sh_doctor_id = fields.Many2one("res.partner", string="Doctor", domain=[(('sh_is_doctor','=', True))], tracking=True)

    sh_precription = fields.Binary(string='Prescription', tracking=True)

    sh_mobile_number = fields.Char("Mobile Number")

    sh_card = fields.Char(string="Aadhar Card",size=12,tracking=True)

    sh_email = fields.Char("Email")

    sh_is_narcotic = fields.Boolean()

    def sh_split_action(self):
        print("\n\n\n Split called \n\n\n")
        return {
            'type': 'ir.actions.act_window',
            'name': _('Split Order'),   #type:ignore
            'res_model': 'sh.split.wizard',
            'target': 'new',
            'view_mode': 'form',
            'view_id':self.env.ref('sh_pharmacy_management_system.sh_split_wizard_view_form').id,            
            'context':{'default_sh_order_line_ids':self.order_line.filtered(lambda rec: rec.select_bool == True).ids
            } 
                       
        }
    
    def sh_calculate_commission(self):
        if self.sh_doctor_id.sh_commission_types=='fixed':
            return self.sh_doctor_id.sh_amount
        elif self.sh_doctor_id.sh_commission_types=='percent':
            return (self.amount_untaxed*self.sh_doctor_id.sh_commission_percent)/100

    def action_confirm(self):
        result = super(ShSaleOrderInherit, self).action_confirm()
        print("\n\n\n in action confirm")

        if self.sh_doctor_id.sh_commission_types!='none':
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
    

    

    

