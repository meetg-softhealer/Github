# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,_ #type:ignore
from odoo.exceptions import UserError #type:ignore
from odoo.osv import expression #type:ignore

class ShProductTemplateInherit(models.Model):
    _inherit = "product.template"

    sh_medicine_form_id = fields.Many2one("sh.medicine.form", string="Product Form", tracking=True)
    sh_ingredients_ids = fields.Many2many("sh.ingredients", string="Ingredients", tracking=True)

    sh_is_medicine = fields.Boolean(default=False, string="Is medicine")
    sh_is_narcotic = fields.Boolean(default=False)

    @api.onchange('categ_id')
    def _onchange_categ_id(self):
        if self.categ_id.sh_is_medicine:
            self.sh_is_medicine = True
        else:
            self.sh_is_medicine = False

        if self.categ_id.sh_is_narcotic:
            self.sh_is_narcotic = True
        else:
            self.sh_is_narcotic = False


    @api.model_create_multi
    def create(self, values):
            
        result = super(ShProductTemplateInherit, self).create(values)
        # print("\n\n self",self)
        # print("\n\n self",values)
        # print("\n\n self",result)
        if result.sh_medicine_form_id:
            result['name'] = result['name']+" "+result.sh_medicine_form_id.name

        return result


    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=None):
        args = list(args or [])
        if not name:
            # When no name is provided, call the parent implementation
            return super().name_search(name=name, args=args, operator=operator,
                                        limit=limit)
        # Add search criteria for name, email, and phone
        domain = ['|',
                    ('name', operator, name),
                    ('sh_ingredients_ids.name', operator, name)
                ]

        records = self.search_fetch(domain, ['display_name'], limit=limit)
        sh_list = [(record.id, record.display_name) for record in records.sudo()]

        res = super().name_search(name=name, args=args, operator=operator,
                                      limit=limit)
        
        for rec in sh_list:
            res.append(rec)
        
        return res    