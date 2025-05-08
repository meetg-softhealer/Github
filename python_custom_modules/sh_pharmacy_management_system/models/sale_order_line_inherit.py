# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,Command,_ #type:ignore
from odoo.exceptions import UserError #type:ignore

class ShSaleOrderLineInherit(models.Model):
    _inherit = "sale.order.line"

    select_bool = fields.Boolean(" ")
    # sh_lot_no = fields.Char(string="Lot/Sr no.", tracking=True)
    # sh_expiry_date = fields.Date(string="Expiry Date", tracking=True)
    sh_lot_no_ids = fields.Many2many("stock.lot",string="Lot/Sr No.", tracking=True)

    sh_total_pdt_qty = fields.Float(default=lambda self:self.product_uom_qty)

    @api.onchange('product_id','product_uom_qty')
    def _onchange_product_id_product_uom_qty(self):
        sh_list = []
        self.sh_total_pdt_qty = self.product_uom_qty
        sh_product_lot_ids = self.env['stock.lot'].search([('product_qty','>',0),('product_id','=',self.product_id.id)])
        # print("\n\n\n product_lot_ids", sh_product_lot_ids)
        if sh_product_lot_ids:             
            for record in sh_product_lot_ids:
                if self.sh_total_pdt_qty > record.product_qty:
                    self.sh_total_pdt_qty -= record.product_qty
                    sh_list += [record.id]        
                else:
                    sh_list += [record.id]
                    break
            print("\n\n\n sh_list", sh_list)
            self.sh_lot_no_ids = [(6,False,sh_list)]


    