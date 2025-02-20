# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api #type:ignore
from odoo.exceptions import UserError, ValidationError #type:ignore


class Animal(models.Model):
    _name = "sh.animal"
    _description = "Animal"

    height = fields.Float(string="Height")

class Dog(models.Model):
    _name = "sh.animal.dog"
    _inherit = "sh.animal"

    sound = fields.Char(string="Sound")
    food  = fields.Char(string="Food")

class Cat(models.Model):
    _name = "sh.animal.cat"
    _inherit = "sh.animal"

    sound = fields.Char(string = "Sound")
    sleeping_time = fields.Char(string="Sleeping Time")

class Animal_More(models.Model):
    _inherit = "sh.animal"

    weight = fields.Float(string="Weight")

class Animal_extra(models.Model):

    _name = "sh.animal"
    _inherit = "sh.animal"

    color = fields.Float(string="Color")