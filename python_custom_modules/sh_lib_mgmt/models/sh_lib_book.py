# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api #type:ignore
from odoo.exceptions import UserError, ValidationError #type:ignore


class books(models.Model):
    _name = "sh.library.book"
    _description = "Book Table"

    name = fields.Char("Book Name")
    isbn = fields.Char("ISBN Number")
    published_date = fields.Date("Pulished Date")
    category_id = fields.Many2one("sh.library.category", string="Category")    
    total_qty = fields.Integer("Total Quantity")   
    borrower_ids = fields.Many2many("sh.library.member", string="Borrower") 
    available_copies = fields.Integer(compute='_compute_available_copies', string="Available Copies")
    availibility = fields.Selection(selection=[('available','Available'),('borrowed','Borrowed')], compute='_compute_borrow_book')

    @api.model_create_multi
    def create(self, vals_list):  
        for rec in vals_list:
            if rec["category_id"]:
              result = super(books, self).create(vals_list)
              return result
            else:
                raise ValidationError("Please fill in the Category field.")

    @api.onchange('name')
    def book_category_check(self):
        if self.name:
            category_id=self.env['sh.library.category'].search([])
            for char in str(self.name).split(' '):
                for data in category_id:
                    if data.name.lower() in char.lower():
                        self.category_id=data.id
                    elif data.name.lower() in self.name.lower():
                        self.category_id=data.id

    # @api.onchange('name')
    # def _onchange_book_ids(self): 
    #     if "science" in str(rec.name) or "Science" in str(rec.name):
    #     rec.category_id = rec.category_id.id
    #     print("science", rec.category_id.name)
    # elif "fiction" in str(rec.name) or "Fiction" in str(rec.name):
    #     rec.category_id = 2 
    #     print("fiction", rec.category_id.name)
    # # else:
    # #     rec.category_id.name = rec.category_id.name
    # #     print("else",rec.category_id.name)normal


    def unlink(self):
        if not self.borrower_ids:
            rec = super(books, self).unlink()
            return rec
        else:
            raise UserError('You cannot delete a book which is already being borrowed!!!')

    @api.depends('total_qty')       
    def _compute_borrow_book(self):           
        for rec in self:
            if len(rec.borrower_ids) < rec.total_qty:
                rec.availibility = 'available'
            elif len(rec.borrower_ids) > rec.total_qty:
                raise UserError('You cannot add a borrower as all the books are already being borrowed!!!') 
            else:    
                rec.availibility = 'borrowed'
            
    @api.depends('total_qty')
    def _compute_available_copies(self):
        for record in self:
            record.available_copies = record.total_qty - len(record.borrower_ids)

    @api.onchange('borrower_ids')
    def _onchange_availibility(self):
        if len(self.borrower_ids) > self.total_qty:
            raise UserError('You cannot add a borrower as all the books are already being borrowed!!!') 
            
            
            
            