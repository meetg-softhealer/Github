# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api #type:ignore

class student(models.Model):
    _name = "sh.student"
    _description = "SH Student"

    name = fields.Char("Name", required=True)
    age = fields.Integer("Age", required=True)
    age_category_id = fields.Many2one("sh.age.category", string="Age Category")

    @api.model_create_multi
    def create(self, vals_list): 
        for rec in vals_list:
            if rec['age']:
                category = self.env['sh.age.category'].search([('min_age','<=',rec['age']),('max_age','>=',rec['age'])])
                rec['age_category_id'] = category.id 
        
        result = super(student, self).create(vals_list)
        return result


class age_category(models.Model):
    _name = "sh.age.category"
    _description = "Age Category"

    name = fields.Char("Name", required=True)
    min_age = fields.Integer("Min Age", required=True)
    max_age = fields.Integer("Max Age", required=True)


    


    