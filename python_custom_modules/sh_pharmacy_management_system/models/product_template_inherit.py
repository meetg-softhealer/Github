# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,_ #type:ignore
from odoo.exceptions import UserError #type:ignore

class ShProductTemplateInherit(models.Model):
    _inherit = "product.template"

    sh_medicine_form_id = fields.Many2one("sh.medicine.form", string="Product Form", tracking=True)
    sh_ingredients_ids = fields.Many2many("sh.ingredients", string="Ingredients", tracking=True)

    is_medicine = fields.Boolean(default=False, string="Is medicine")

    @api.onchange('categ_id')
    def _onchange_categ_id(self):
        if self.categ_id.sh_is_medicine:
            self.is_medicine = True
        else:
            self.is_medicine = False

    @api.model_create_multi
    def create(self, values):
            
        result = super(ShProductTemplateInherit, self).create(values)
        # print("\n\n self",self)
        # print("\n\n self",values)
        # print("\n\n self",result)
        if result.sh_medicine_form_id:
            result['name'] = result['name']+" "+result.sh_medicine_form_id.name

        return result
