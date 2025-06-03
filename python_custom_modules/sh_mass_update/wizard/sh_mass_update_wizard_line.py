# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,_ #type:ignore
from odoo.exceptions import UserError #type:ignore

class ShMassUpdateWizardLine(models.TransientModel):
    _name = "sh.mass.update.wizard.line"

    sh_mass_update_wizard_id = fields.Many2one("sh.mass.update.wizard")

    sh_current_model = fields.Many2one("ir.model", string="Current Model", related='sh_mass_update_wizard_id.sh_current_model', readonly=True)

    sh_field_ids = fields.Many2many("ir.model.fields", 
    domain=[('ttype','in',['char','datetime','float','html','integer','text','binary']), 
            ('readonly','=',False)]
    )

    @api.onchange('sh_current_model')
    def _onchange_sh_current_model(self):
        sh_type_list = ['char','datetime','float','html','integer','text','binary']
        self.sh_field_ids = [(4,rec.id) for rec in self.sh_current_model.field_id
                              if rec.ttype in sh_type_list 
                              and rec.readonly==False]