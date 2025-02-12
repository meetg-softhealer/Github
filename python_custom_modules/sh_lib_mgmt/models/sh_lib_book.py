# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api #type:ignore
from odoo.exceptions import ValidationError #type:ignore


class books(models.Model):
    _name = "sh.library.book"
    _description = "Book Table"

    name = fields.Char("Book Name")
    category_id = fields.Many2one("sh.library.category", string="Category")    
    borrower_ids = fields.Many2many("sh.library.member", string="Borrower") 

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
                
