# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,_ #type:ignore
from odoo.exceptions import UserError #type:ignore

class ResPartnerInherit(models.Model):
    _inherit = "res.partner"

    #for Doctors
    sh_is_doctor = fields.Boolean()

    sh_gender = fields.Selection(selection=[('male','Male'),('female','Female')],string="Gender", required=True, tracking=True)
    sh_specialization_ids = fields.Many2many("sh.specialization",string="Specialization")

    # sh_commission_type = fields.Many2one("sh.commission.type", string="Commission Type",tracking=True, required=True)

    sh_commission_types = fields.Selection([('fixed','Fixed'),('percent','Percentage'),('none','None')], string="Commission Type", default='none', required=True, trackable=True)    
    sh_amount = fields.Monetary("Amount", tracking=True, required=True)
    sh_commission_percent = fields.Float("Commission Rate(%)", tracking=True, required=True)

    sh_commission_ids = fields.One2many("sh.doctor.commission","sh_res_partner_id")
    # sh_designation = fields.Char("Specialization")

    #for Patients

    sh_card = fields.Char(string="Aadhar Card",size=12,tracking=True)
    sh_dob = fields.Date(string="Date of Birth", tracking=True)
    sh_blood = fields.Selection(string="Blood Type",selection=[('a','A'),('b','B'),('o','O'),('ab','AB'),('apositive','A+'),('bpositive','B+'),('opositive','O+'),('abpositive','AB+'),('anegetive','A-'),('bnegetive','B-'),('onegetive','O-'),('abnegetive','AB-')], tracking=True)
    sh_age = fields.Integer(string="Age", tracking=True)
    sh_allergies_ids = fields.Many2many("sh.allergies", string="Allergies", tracking=True)


    def sh_create_commission_line(self):
        print("\n\n\n com line called")
        print("\n\n\n self id", self.id)
        
        record_ids = self.env['sh.doctor.commission'].search([('sh_res_partner_id','=',self.id)])
        print("\n\n\n record ids", record_ids)
        self.sh_commission_ids = [(4,rec.id) for rec in record_ids]
        print("\n\n\n commission ids",self.sh_commission_ids)