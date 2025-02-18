# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
import datetime as dt
from odoo import models,fields,api #type:ignore
from odoo.exceptions import UserError, ValidationError #type:ignore


class Employee(models.Model):
    _name="sh.employee"
    _description="Employee Management"
    _inherit=['mail.thread','mail.activity.mixin']

    name=fields.Char(string="Employee Name",required=True)
    employee_image=fields.Image()
    mobile = fields.Char("Mobile")
    ###[Relational]
    category_ids=fields.Many2many("sh.employee.category",string="Category")
    department_id=fields.Many2one("sh.department")
    job_id=fields.Many2one("sh.job",string="Jobs")
    job_position=fields.Many2one("sh.employee.jobs",string="Job Position")
    employee_id=fields.Many2one("sh.employee",string="Team Leader")
    user_id=fields.Many2one("res.users",string="User")
    tz = fields.Char(string="Timezone")
    country_of_birth=fields.Many2one('res.country',string="Place of Birth")
    country_id=fields.Many2one('res.country',string="Country")

    category_id = fields.Many2one('sh.employee.category', string="Category")
    ref = fields.Char("ref", readonly=True)
    

    ###[Work Info]
    employee_badge_no=fields.Char(string="Employee ID")
    work_address=fields.Text(string="Work Address")
    work_email=fields.Char(string="Work Email")
    work_phone=fields.Char(string="Work Phone")
    working_time=fields.Char(string="Working Hours")
    total_leave=fields.Float(string="Leaves")
    
    ###[private]
    birthdate=fields.Date(string="BirthDate")
    age=fields.Integer(string="Age",compute="_compute_age_calculation")
    gender=fields.Selection("Selection_Dynamic",string="Gender",default="male")
    # height=fields.Float(string="Height")
    # weight=fields.Float(string="Weight")
    blood_group=fields.Selection(string="Blood Group",selection=[('a','A'),('b','B'),('o','O'),('ab','AB'),('apositive','A+'),('bpositive','B+'),('opositive','O+'),('abpositive','AB+'),('anegetive','A-'),('bnegetive','B-'),('onegetive','O-'),('abnegetive','AB-')])
    marital_status=fields.Selection(string="Marital Status",selection=[('married','Married'),('unmarried','Unmarried'),('divorced','Divorced'),('widower','Widower')])
    private_email=fields.Char(string="Personal Email Id")
    private_mo_number=fields.Char(string="Mobile Number")
    
    
    ###[Other Info]
    ###[Address]
    private_address=fields.Text(string="Address")
    city=fields.Char(string="City")
    pincode=fields.Char(string="Pin Code")
    state=fields.Char(string="State")
     ###[Education]
    educational_background=fields.Char()
    graduation_level=fields.Selection(selection=[('bachelor','Bachelor'),('master','Master'),('phd','PHD')])
    
    
    ###[Employee Info]
    joining_date=fields.Date(string="Joining Date")
    branch_name=fields.Char(string="Branch Name")
    years_of_experience=fields.Float(string="Experience")
    salary=fields.Float(string="Salary")
    id_proof_number=fields.Char()
    skills=fields.Many2many("sh.employee.skill")
    last_company_name=fields.Char()
    last_job_position=fields.Char()
    
    ###[Bank]
    bank_account_no=fields.Char()
    bank_account_name=fields.Char()
    bank_ifsc_code=fields.Char()
    bank_account_type=fields.Selection(selection=[('neft','NEFT'),('imps','IMPS'),('rtgs','RTGS')])
    ###[Documents]
    resume=fields.Binary(string="Resume")
    security_documents=fields.Many2many('ir.attachment',string="Security Documents")
   

    def Multi_Update_Methods(self):
        records=self.search([],limit=5)
        print(records)
        records.write({"name":"Bhavin"})
        return records
    def Selection_Dynamic(self):
        List=[('male','Male'),('female','Female'),('other','Other')]
        return List
    @api.depends('birthdate')
    def _compute_age_calculation(self):
        today_date=dt.datetime.today()
        for records in self:
            birth_date=fields.Datetime.to_datetime(records.birthdate)
            if birth_date:
                total_age=str(int((today_date - birth_date).days / 365))
                records.age=total_age
            else:
                records.age = 0
        
    @api.onchange('user_id')
    def _onchange_user_id(self):
        self.name = self.user_id.name
        self.tz = self.user_id.tz
    
       
    @api.model_create_multi
    def create(self, vals_list):  
        # print(val)  
        for rec in vals_list:
            # print(rec)
            for k,v in rec.items():
                # print(k,v)
                if str(k)=="name":
                    rec[k] = rec[k].upper()
        
        for rec in vals_list:
            if rec["mobile"]:
                if '+91' not in rec["mobile"][0:3]:
                    rec["mobile"] = '+91 '+rec["mobile"]

        for rec in vals_list:
            email = self.search([('work_email',"=",rec['work_email'])])
            if email:
                raise UserError("Email already exists")

        result = super(Employee, self).create(vals_list)

        # print("\n\n\n\n\=======================\n\n\n\n\n")
        # print(self)
        result.ref = result.category_id.ref
        return result
    
    # @api.onchange('category_id')
    # def _onchange_category_id(self):
    #     if self.category_id:
    #         self.ref = self.category_id.ref


    def write(self, values):
        # print("\n\n\n\n\n\n=======1",self)
        # print("\n\n\n\n\n\n=======2",values)
        
        if "mobile" in values:
            if values["mobile"]:
                # print("In 1st if condition=====3")
                # print(self.mobile)
                if '+91' not in values["mobile"][0:3]:
                    values["mobile"] = '+91 '+values["mobile"]
                    # print(self.mobile)
        result = super(Employee, self).write(values)
        return result
    
    