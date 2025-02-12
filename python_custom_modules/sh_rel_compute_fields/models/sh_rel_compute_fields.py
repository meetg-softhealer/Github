import datetime as dt
from odoo import models,fields,api #type:ignore

class Employee(models.Model):
    _name="sh.rel.compute.fields"
    _description="Relational and compute fields"

    km = fields.Float("Enter Distance(In km)")
    meter = fields.Integer("Distance in meter", compute="_compute_km")

    @api.depends('km')
    def _compute_km(self):
        for rec in self:
            rec.meter = rec.km * 1000 


    kilometer = fields.Float("Enter Kilometer")
    Meters = fields.Float("In Meters", related='kilometer')

    @api.onchange('kilometer')
    def _onchange_field(self):

        self.Meters = self.kilometer * 1000.0
    
    