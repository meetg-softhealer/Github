# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api #type:ignore

class member(models.Model):
    _name = "sh.library.member"
    _description = "Member Table"

    name = fields.Char("Member's Name")
    book_ids = fields.Many2many("sh.library.book", string="Books")
    membership = fields.Selection(selection=[('regular','Regular'),('premium','Premium')], compute='_compute_membership', readonly=True)
   
    @api.depends('book_ids')
    def _compute_membership(self):
        for rec in self:
            if len(rec.book_ids) >= 3:
                rec.membership = 'premium'
            else:
                rec.membership = 'regular'