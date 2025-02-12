# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api #type:ignore

class category(models.Model):
    _name = "sh.library.category"
    _description = "Category Table"

    name = fields.Char("Category Name")
    book_ids = fields.One2many("sh.library.book","category_id",string="Books")
    total_book = fields.Integer("Total Books", compute='_compute_total_books')
    
    @api.depends('book_ids')
    def _compute_total_books(self):
        for rec in self:
            rec.total_book = len(rec.book_ids)
        
    