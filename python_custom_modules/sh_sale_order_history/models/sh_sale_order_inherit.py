# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api #type:ignore
from odoo.exceptions import UserError, ValidationError #type:ignore
from dateutil.relativedelta import relativedelta 
from datetime import datetime

class sh_sale_order_inherit(models.Model):
    _inherit = "sale.order"

    sale_order_line_ids = fields.One2many("sale.order.line", "sale_order_id", string="Sale Orders")
    # res_company_id = fields.Many2one("res.company")
    # temp_table_ids = fields.Many2many("temp.table", related='company_id.sh_stage_ids')
    

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        print("\n\n\n\n\n\n\n=====",self.env.user.company_id.sh_last_no_of_orders)

        if self.env.user.company_id.sh_enable_reorder:
            # print("\n\n\n\n\n\n==========days",self.env.user.company_id.sh_last_no_of_days)
            # print("\n\n\n\n\n\n\n=====",self.env.user.company_id.sh_stage_ids.tech_name)
            # print("\n\n\n\n\n\n\n=====",datetime.today()-relativedelta(days=self.env.user.company_id.sh_last_no_of_days))
            
            record_ids = self.search(domain=[('partner_id','=',self.partner_id.id),
                                             ('date_order','>=',datetime.today()-relativedelta(days=self.env.user.company_id.sh_last_no_of_days)),
                                            #  ('state','in',[t_name.tech_name for t_name in self.env.user.company_id.sh_stage_ids])],
                                             ('state','in',self.env.user.company_id.sh_stage_ids.mapped('tech_name'))],
                                    limit=self.env.user.company_id.sh_last_no_of_orders)

            # print("\n\n\n\n\n\n=========",record_ids)

            for order in record_ids:
                print('\n\n\n\n\n\n==== In :Loop')
                self.sale_order_line_ids += order.order_line


    def reorder_button_action(self):
        # record_list = []
        # for rec in self.sale_order_line_ids:
        #     if rec.select_bool:
        #         record_list += rec                

        # self.create_new_record(record_list)
        for record in self.sale_order_line_ids:
            if record.select_bool:
                record.env['sale.order.line'].create({'order_id':self.id,
                                                  'product_id':record.product_template_id.id,                                                  
                                                })
        
        self.sale_order_line_ids.select_bool = False




    



    