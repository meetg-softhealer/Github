# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,_ #type:ignore 
from odoo.exceptions import UserError #type:ignore

class ShMedicineForm(models.Model):
    _name = "sh.medicine.form"

    name = fields.Char("Medicine Form")