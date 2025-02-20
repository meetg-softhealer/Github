# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api #type:ignore
from odoo.exceptions import UserError, ValidationError #type:ignore


class sh_note(models.Model):
    _name = "sh.note"
    _description = "SH Note"

    name = fields.Char("Name")

class sh_inherit_sale_order(models.Model):
    _inherit = "sale.order"
    _description = "Sale order inherited"

    custom_note_ids = fields.Many2many("sh.note", string="Custom Note")

class sh_inherit_sale_order_line(models.Model):
    _inherit = "sale.order.line"
    _description = "Sale order line inherited"

    custom_note_id = fields.Many2one("sh.note", string="Note")