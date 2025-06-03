# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,_ #type:ignore
from odoo.exceptions import UserError #type:ignore


class ShMassUpdateWizard(models.TransientModel):
    _name = "sh.mass.update.wizard"

    sh_current_model = fields.Many2one("ir.model", string="Current Model")

    

    def sh_create_recs(self):
        for record in self.sh_field_ids:
            print("\n\n\n")
            for rec in record:
                print(rec)
            print("\n\n\n")
    