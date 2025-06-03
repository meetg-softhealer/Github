# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,_ #type:ignore
from odoo.exceptions import UserError, ValidationError #type:ignore


class SaleOrder(models.Model):
    _inherit = "sale.order"

    sh_current_model = fields.Many2one("ir.model", string="Current Model")

    def sh_mass_update_action(self):

        print("\n\n\n active model ", self.env.context.get('active_model'), "\n\n\n")

        return {
            'type': 'ir.actions.act_window',            
            'res_model': 'sh.mass.update.wizard',        
            'view_mode': 'form',
            'views_type': 'form',
            'target':'new',
            'view_id': self.env.ref('sh_mass_update.sh_mass_update_wizard_view_form').id,
            'context':{'default_sh_current_model':self.env['ir.model'].search([('model','=',self.env.context.get('active_model'))]).id,
                       } 
        }
    