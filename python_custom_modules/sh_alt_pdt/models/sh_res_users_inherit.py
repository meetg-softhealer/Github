# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,_ #type:ignore
from odoo.exceptions import UserError #type:ignore


class res_user_inherit(models.Model):
    _inherit = "res.users"

    alt_pdt_bool = fields.Boolean(string="Manage Alternative Products")


        