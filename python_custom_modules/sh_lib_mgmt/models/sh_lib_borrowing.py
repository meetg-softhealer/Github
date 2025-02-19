# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api #type:ignore
from odoo.exceptions import UserError, ValidationError #type:ignore


class borrowing(models.Model):
    _name = "sh.library.borrowing"
    _description = "Borrowing Table"

    member_id = fields.Many2one("sh.library.member", string="Member", required=True)
    book_id = fields.Many2one("sh.library.book", string="Book", required=True)
    borrow_date = fields.Date("Borrow Date", required=True)
    return_date = fields.Date("Return Date")
    state = fields.Selection(string="Book State", selection=[('borrowed', 'Borrowed'),('returned','Returned')], required=True)

    @api.model_create_multi
    def create(self, vals_list): 
        for rec in vals_list:
            available_book = self.env['sh.library.book'].browse(rec['book_id'])
            if rec['state']=='borrowed':
                if 'available' in available_book.availibility:
                    available_book.available_copies -= 1
                    available_book.borrower_ids = [(4,rec['member_id'])]
                else:
                    raise UserError("The book is not available to be borrowed!!!")

        result = super(borrowing, self).create(vals_list)
        return result

    def write(self, values):
        # available_book = self.env['sh.library.book'].browse(self.book_id)
        # member = self.env['sh.library.member'].browse([self.member_id])
        
        if 'book_id' in values or 'member_id' in values:
            raise UserError("Name or Book can't be changed!!!")
        
            
        if values['state']=='returned':
            # print(self.book_id.id)
            # print(self.member_id.id)

            available_book = self.env['sh.library.book'].browse(self.book_id.id)
            available_book.available_copies += 1

            member = self.env['sh.library.member'].browse(self.member_id.id)
            member.book_ids = [(3,self.book_id.id)]
                


        result = super(borrowing, self).write(values)
        return result