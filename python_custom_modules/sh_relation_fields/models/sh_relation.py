# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
import datetime as dt
from odoo import models,fields,api # type: ignore

class Patient(models.Model):
    _name = "sh.patient"
    _decription = "Patient Table"

    name = fields.Char("Name")
    age = fields.Integer("Age")
    doctor_id = fields.Many2one("sh.doctor")
    diagnosis_ids = fields.Many2many("sh.diagnosis", "patient_diagnosis", string="Diagnosis") 

class Doctor(models.Model):
    _name = "sh.doctor"
    _description = "Doctor Table"

    name = fields.Char("Doctor")
    specialization = fields.Char("Specialization")
    patient_ids = fields.One2many("sh.patient","doctor_id",string="Patients")

class Diagnosis(models.Model):
    _name = "sh.diagnosis"
    _description = "Diagnosis Table"

    name = fields.Char("Diagnosis")
    patient_ids = fields.Many2many("sh.patient",string="Patients")
