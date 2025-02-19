# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api #type:ignore
from odoo.exceptions import UserError, ValidationError #type:ignore


class member(models.Model):
    _name = "sh.library.member"
    _description = "Member Table"

    name = fields.Char("Member's Name")
    membership_id = fields.Char("Membership ID")
    phone = fields.Char("Phone")
    email = fields.Char("Email")
    already_a_mobile = fields.Boolean("Already a Number?", readonly=True)
    book_ids = fields.Many2many("sh.library.book", string="Books")
    membership = fields.Selection(selection=[('regular','Regular'),('premium','Premium')], compute='_compute_membership', readonly=True)

    @api.depends('book_ids')
    def _compute_membership(self):
        for rec in self:
            if len(rec.book_ids) >= 3:
                rec.membership = 'premium'
            else:
                rec.membership = 'regular'  

    @api.model_create_multi
    def create(self, vals_list): 
        for rec in vals_list:       
            mobile = self.search([('phone','=',rec['phone'])])
            membership = self.search([('membership_id','=',rec['membership_id'])])
            if mobile:                
                rec['already_a_mobile'] = True
            if membership:
                raise UserError("The Membership Id already exists")
            
        result = super(member, self).create(vals_list)
        return result
                
    def write(self, values):
        # print("\n\n\n\n\n\n=======1",self)
        # print("\n\n\n\n\n\n=======2",values)
        # print(self.phone)
        if 'phone' in values:
            mobile = self.search([('phone','=',values['phone'])])
            if mobile:                
                values['already_a_mobile'] = True

        if 'membership_id' in values:
            membership = self.search([('membership_id','=',values['membership_id'])])
            if membership:
                raise UserError("The Membership Id already exists")

        result = super(member, self).write(values)
        return result