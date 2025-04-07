# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,_ #type:ignore
from odoo.exceptions import UserError, ValidationError #type:ignore
from odoo.osv import expression #type:ignore

class sh_calendar_inherit(models.Model):
    _inherit = "calendar.event"

    project_id = fields.Many2one('project.project', string='Project')
       
    task_id = fields.Many2one("project.task", string="Task")

    timesheet_ids = fields.One2many('account.analytic.line','calendar_id')
    
    update_reason = fields.Char("Reason for Update Time")

    update_bool =  fields.Boolean(default=False)
    update_bool2 = fields.Boolean(default=False)

    def create(self, values):
            
        
        result = super(sh_calendar_inherit, self).create(values)

        for people in result.partner_ids.employee_ids:
          self.env['account.analytic.line'].create({'calendar_id':result.id,
                                                    'date':result.start,
                                                    'project_id':result.project_id.id,
                                                    'task_id':result.task_id.id,
                                                    'employee_id':people.id,
                                                    'name':result.name,
                                                    'unit_amount':result.duration})
        result.update_bool = True
      
        return result     
    
    @api.model
    def write(self, values):
      
      result = super(sh_calendar_inherit, self).write(values)
      
      rec = self.env['account.analytic.line'].search([('calendar_id','=',self.id)])
      
      if 'start' in values:
        self.update_bool2 = True
        rec.write({'date':self.start.date(),
                       'unit_amount':self.duration}) 
        
        
      if 'stop' in values:
        self.update_bool2 = True
        rec.write({'date':self.start.date(),
                       'unit_amount':self.duration}) 
        
      return result