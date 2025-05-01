# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,_ #type:ignore 
from odoo.exceptions import UserError #type:ignore

class ShStockLotInherit(models.Model):
    _inherit = "stock.lot"

    def _compute_display_name(self):
        print("\n\n compute called \n\n")
        for rec in self:
            rec.display_name = f"[{rec.name}] {str(rec.expiration_date)}"        