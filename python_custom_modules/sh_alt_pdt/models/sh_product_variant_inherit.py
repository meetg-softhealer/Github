# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,_ #type:ignore
from odoo.exceptions import UserError #type:ignore

class sh_product_variant_inherit(models.Model):
    _inherit = "product.product"

    alt_pdt_ids = fields.Many2many("product.product", string="Alterntive Product",relation="pdt_pdt", column1='source_id', column2='destination_id')

    @api.model
    def create(self,vals_list):

        rtn = super(sh_product_variant_inherit, self).create(vals_list)
        # print("\n\n\n\n\n\n=======",rtn)
        # print("\n\n\n\n\n\n=======",rtn.alt_pdt_ids)
        if vals_list.get('alt_pdt_ids'):
                # print("\n\n\n\n\n\n=========",vals_list.get('alt_pdt_ids'))
                # print("\n\n\n\n\n\n=========",self.alt_pdt_ids.ids)
                for rec in rtn.alt_pdt_ids:
                    # print("\n\n\n\n\n\n=========",rec)

                    # print("\n\n\n\n\n\n=======",[(4,id,False) for id in rec.alt_pdt_ids.ids])
                    # print("\n\n\n\n\n\n========= create",[(4,item.id) for item in rtn.alt_pdt_ids])
                    if not self.env.context.get('duplicate'):
                        rec.write({                
                        'alt_pdt_ids': [(4,item.id) for item in rtn.alt_pdt_ids if item.id != rec.id]+[(4,rtn.id,False)] #(6,False,rtn.alt_pdt_ids.ids)
                                        # (3,rec.id,False),
                                        # (4,rtn.id,False)]
                        })
        return rtn



    # @api.onchange('alt_pdt_ids')
    # def _onchange_alt_pdt_ids(self): 
    #     # if self.alt_pdt_ids:
    #     #     print("\n\n\n\n\n=======write", self.alt_pdt_ids)
    #     for rec in self.alt_pdt_ids:
    #         print("\n\n\n\n\n\n========in loop",rec)
    #         # rec.alt_pdt_ids = [self.id] 
    #         rec.write({                
    #         'alt_pdt_ids': [(3,rec.id,False)]
    #         })
                      
     
   
    def write(self, values):
           
        print(values)
        if values.get('alt_pdt_ids'):
            for x in values['alt_pdt_ids']:
                if x[0]==3:
                    if not self.env.context.get('repeat'):

                        record = self.browse(x[1])
                        record.with_context(repeat=True).write({
                            'alt_pdt_ids': [(5,False,False)]
                        })
        
        result = super(sh_product_variant_inherit, self).write(values)
    
        if values.get('alt_pdt_ids'):
            print(self.alt_pdt_ids)
            
            for rec in self.alt_pdt_ids:            
                
                if not self.env.context.get('duplicate'):
                    # print("\n\n\n\n\n\n=======",[(4,id,False) for id in rec.alt_pdt_ids.ids])
                    # print("\n\n\n\n\n\n========= write",[(4,item.id) for item in self.alt_pdt_ids])
                    rec.with_context(duplicate=True).write({                
                    'alt_pdt_ids': [(4,item.id) for item in self.alt_pdt_ids if item.id != rec.id]+[(4,self.id,False)] #(6,False,self.alt_pdt_ids.ids)                                                                    
                    })

        return result
    

        



    # def alt_pdt_bool(self):
    #     print("\n\n\n\n\n\n self ", self)
    #     current_user_bool = self.env.user.alt_pdt_bool
    #     print("\n\n\n\n\n=======", current_user_bool)

    #     return current_user_bool
    
    