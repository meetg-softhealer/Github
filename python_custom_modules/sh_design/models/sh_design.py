# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api #type:ignore
from odoo.exceptions import UserError, ValidationError #type:ignore


class partner_inherit(models.Model):

    _inherit = "res.partner"

    design_ids = fields.One2many('sh.design', 'partner_id', string="Designs")
    

class Design(models.Model):
    _name = "sh.design"

    partner_id = fields.Many2one(comodel_name="res.partner", string="Partner")

    design_category_id = fields.Many2one("sh.design.category", string="Category")
    design_type_id = fields.Many2one("sh.design.type", string="Type")
    des_typ_img = fields.Image(related='design_type_id.img')
