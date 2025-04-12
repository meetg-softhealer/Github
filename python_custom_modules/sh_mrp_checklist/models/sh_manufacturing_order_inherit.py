# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,_ #type:ignore
from odoo.exceptions import UserError #type:ignore
import base64
import csv
import io
import xlrd 

class ManufacturingOrdersInherit(models.Model):
    _inherit = "mrp.production"

    manufacturing_checklist_template_ids = fields.Many2many("manufacturing.checklist.template",string="Checklist Templates")

    manufacturing_order_line_ids = fields.One2many("manufacturing.order.checklist.line","manufacturing_order_id")
    
    checklist_completed = fields.Integer("Checklist Completed",compute='_compute_checklist_completed', search='_search_checklist_completed')
        
    def _search_checklist_completed(self, operator, value):
        if operator == '=':
            operator = '=='
            mo = self.search([]).filtered(lambda p: eval(f"p.checklist_completed {operator} {value}"))
            return [('id', 'in', mo.ids)]
        else:
            operator = "!="
            mo = self.search([]).filtered(lambda p: eval(f"p.checklist_completed {operator} {value}"))
            return [('id', 'in', mo.ids)]
        # mo = self.search([])
        # id_list = []

        # for record in mo:
                   
        #     print("\n\n\n\n method call")  
        #     if operator == '=' and value:
        #         print("\n\n\n\n in if")  
        #         for task in mo.manufacturing_order_line_ids:                                        
        #             print("\n\n\n\n in loop")  
        #             if task.checklist_completed == 100:
        #                 print("\n\n\n\n in 2nd if")  
        #                 id_list.append(task.manufacturing_order_id.id)    
        #                 print("\n\n\n\n",id_list)  
            
        # return [('id', 'in', id_list)]
    

    def _compute_checklist_completed(self):        
        for record in self:
            complete_counter = 0
            if record['manufacturing_order_line_ids']:
                for rec in record['manufacturing_order_line_ids']:
                    if rec.state == 'complete':
                        complete_counter += 1

                complete_percent = (complete_counter/len(record.manufacturing_order_line_ids))*100    
                record.checklist_completed = complete_percent
            else:
                record.checklist_completed = complete_counter
        
        
        # complete_counter = 0
        # if self.manufacturing_order_line_ids:
        #     for record in self.manufacturing_order_line_ids:
        #         if record.state == 'complete':
        #             complete_counter += 1

        #     complete_percent = (complete_counter/len(self.manufacturing_order_line_ids))*100
        #     self.checklist_completed = complete_percent
        # else:
        #     self.checklist_completed = complete_percent
    
    
    
    @api.onchange('manufacturing_checklist_template_ids')
    def _onchange_manufacturing_checklist_template_ids(self):
                       
        self.manufacturing_order_line_ids = [(5,0,0)]
        
        if self.manufacturing_checklist_template_ids.check_list_ids:
            for rec in self.manufacturing_checklist_template_ids.check_list_ids:
                if rec.id not in self.manufacturing_order_line_ids.ids:
                    print("\n\n\n\n name",rec.name)
                    print("\n\n\n\n ",rec.id)
                    dict1 = {
                        'checklist_id':rec.id,
                        'description':rec.description,
                        'date':self.date_start,
                        'state':'new'
                    }
                    self.manufacturing_order_line_ids = [(0,0,dict1)]

            
    # def import_files(self):
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'name': _('Import files'),   #type:ignore
    #         'res_model': 'import.wizard',
    #         
    #         'view_mode': 'form',
    #     }