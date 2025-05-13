# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,_,Command #type:ignore
from odoo.exceptions import UserError #type:ignore
import xlwt #type:ignore
import io
import xlsxwriter #type:ignore
import base64
from datetime import datetime
from datetime import date
from dateutil.relativedelta import relativedelta

class ShPharmacyReportWizard(models.TransientModel):
    _name = "sh.pharmacy.report.wizard"

    # Report Booleans
    sh_is_fetch = fields.Boolean()
    sh_is_cash_drawer = fields.Boolean()
    sh_is_exp_date = fields.Boolean()
    sh_is_doctor_commission = fields.Boolean()
    sh_is_product_selling = fields.Boolean()
    sh_is_fsn = fields.Boolean()
    sh_is_patient = fields.Boolean()


    sh_wiz_from_date = fields.Datetime("From:", default=datetime.today()-relativedelta(months=1))    

    sh_wiz_to_date = fields.Datetime("To:", default=datetime.today())

    # Cash Drawer Fields
    sh_wiz_cashier_id = fields.Many2one("res.users", string="Cashier")
    sh_cash_drawer_wizard_line_ids = fields.Many2many("sh.cash.drawer.wizard.line")

    # Expiry Date Fields and Product Selling and Fsn Fields
    sh_product_id = fields.Many2one("product.product", string="Product:")
    sh_category_id = fields.Many2one("product.category", string="Category:")
    #Expiry Date
    sh_lot_id = fields.Many2one("stock.lot", string="Batch Number")
    sh_exp_date_wizard_line_ids = fields.Many2many("sh.exp.date.wizard.line", string="") 
    #Product Selling
    sh_product_wizard_line_ids = fields.Many2many("sh.product.wizard.line", string="") 

    #Doctor Commission Fields and Patient Field
    sh_doc_id = fields.Many2one("res.partner", string="Doctor", domain=[('sh_is_doctor','=',True)])
    sh_doctor_commission_wizard_line_ids = fields.Many2many("sh.doctor.commission.wizard.line", string="")

    #Fsn fields
    sh_min_qty_rate = fields.Float("Minimum Qty Rate")
    sh_sale_rate = fields.Selection([('fast','Fast'),('slow','Slow')], string="Sale Rate:")  
    sh_fsn_wizard_line_ids = fields.Many2many("sh.fsn.wizard.line", string="")

    #Patient Fields
    sh_patient_id = fields.Many2one("res.partner", string="Patient")
    sh_age_categ = fields.Selection([('child','0-12'),('teen','13-18'),('adult','19-40'),('senior','40+')], string='Age Category')
    sh_gender = fields.Selection([('male','Male'),('female','Female')], string="Gender")
    sh_patient_wizard_line_ids = fields.Many2many("sh.patient.wizard.line", string="")

    def fetch_report_action(self):
        self.sh_is_fetch = True
        domain = []

        self.sh_cash_drawer_wizard_line_ids = False
        self.sh_exp_date_wizard_line_ids = False
        self.sh_doctor_commission_wizard_line_ids = False
        self.sh_product_wizard_line_ids = False
        self.sh_fsn_wizard_line_ids = False
        self.sh_patient_wizard_line_ids = False
        

        if not self.sh_wiz_from_date or not self.sh_wiz_to_date:
                raise UserError("Enter From and To date fields to generate reports!!!")
        
        if self.sh_is_cash_drawer:

            date_domain = [('start_at','>=',self.sh_wiz_from_date),('stop_at','<=',self.sh_wiz_to_date)]
            
            if self.sh_wiz_cashier_id:
                domain += [(('user_id','=',self.sh_wiz_cashier_id.id))]
            
            records = self.env['pos.session'].search(domain+date_domain)
                
            self.sh_cash_drawer_wizard_line_ids = [Command.create({
                                                    'sh_session_id':rec.id,
                                                    'sh_date':rec.start_at.strftime("%Y-%m-%d"),
                                                    'sh_cashier_id':rec.user_id.id,
                                                    'sh_open_bal':rec.cash_register_balance_start,
                                                    'sh_close_bal':rec.cash_register_balance_end_real,
            }) for rec in records]

            for rec in self.sh_cash_drawer_wizard_line_ids:
                cash_sale = self.env['pos.payment'].search([('payment_method_id.name','=','Cash'),('payment_date','>=',rec.sh_session_id.start_at),('payment_date','<=',rec.sh_session_id.stop_at)])
                cash_sale_total = 0
                for item in cash_sale:
                    cash_sale_total += item.amount
                    print("\n\n Item",item.amount)
                print("\n\n Cash Total",cash_sale_total)
                rec.sh_cash_sale = cash_sale_total

                card_sale = self.env['pos.payment'].search([('payment_method_id.name','=','Card'),('payment_date','>=',rec.sh_session_id.start_at),('payment_date','<=',rec.sh_session_id.stop_at)])
                card_sale_total = 0
                for item in card_sale:
                    card_sale_total += item.amount
                    print("\n\n Item",item.amount)
                print("\n\n Card Total",card_sale_total)
                rec.sh_card_sale = card_sale_total

                upi_sale = self.env['pos.payment'].search([('payment_method_id.name','=','UPI'),('payment_date','>=',rec.sh_session_id.start_at),('payment_date','<=',rec.sh_session_id.stop_at)])
                upi_sale_total = 0
                for item in upi_sale:
                    upi_sale_total += item.amount
                rec.sh_upi_sale = upi_sale_total
                # rec.sh_net_cash = rec.sh_close_bal
        
        if self.sh_is_exp_date:

            if self.sh_wiz_from_date or self.sh_wiz_to_date:
                domain += [('expiration_date','>=',self.sh_wiz_from_date),('expiration_date','<=',self.sh_wiz_to_date)]    
            if self.sh_product_id:
                domain += [('product_id','=',self.sh_product_id.id)]
            if self.sh_category_id:
                domain += [('product_id.categ_id','=',self.sh_category_id.id)]            
            if self.sh_lot_id:
                domain += [('name','=',self.sh_lot_id.name)]

            records = self.env['stock.lot'].search(domain+[('product_qty','>',0)])

            self.sh_exp_date_wizard_line_ids = [Command.create({
                                                'sh_pdt_id':rec.product_id.id,
                                                'sh_lot_name':rec.name,
                                                'sh_exp_date':rec.expiration_date,
                                                'sh_qty':rec.product_qty,                                            
                                                'sh_category_id':rec.product_id.categ_id.id
            }) for rec in records]

            for rec in self.sh_exp_date_wizard_line_ids:
                rec.sh_days_remaining = (rec.sh_exp_date.date() - datetime.now().date()).days
         
        if self.sh_is_doctor_commission:
            
            if self.sh_wiz_from_date or self.sh_wiz_to_date:
                domain += [('date_order','>=',self.sh_wiz_from_date.date()),('date_order','<=',self.sh_wiz_to_date.date())]            
            if self.sh_doc_id:
                domain += [('sh_doctor_id','=',self.sh_doc_id.id)]

            records = self.env['sale.order'].search(domain+[('sh_doctor_id','!=',False)])

            self.sh_doctor_commission_wizard_line_ids = [Command.create({
                                                'sh_so_id':rec.id,
                                                'sh_date':rec.date_order,
                                                'sh_doctor_id':rec.sh_doctor_id.id,
                                                'sh_patient_id':rec.partner_id.id,
                                                'sh_commission_percentage':rec.sh_doctor_id.sh_commission_percent,
                                                'sh_commission_fixed_amount':rec.sh_doctor_id.sh_amount                                                
            }) for rec in records]        

            for record in self.sh_doctor_commission_wizard_line_ids:
                sh_total = 0
                for rec in record.sh_so_id.order_line:
                    sh_total += rec.price_subtotal 
                record.sh_bill_total = sh_total

                if record.sh_doctor_id.sh_commission_types=='percent':
                    record.sh_com_amount = (record.sh_bill_total*record.sh_commission_percentage)/100
                elif record.sh_doctor_id.sh_commission_types=='fixed':
                    record.sh_com_amount = record.sh_commission_fixed_amount

        if self.sh_is_product_selling:

            if self.sh_wiz_from_date or self.sh_wiz_to_date:
                domain += [('order_id.date_order','>=',self.sh_wiz_from_date.date()),('order_id.date_order','<=',self.sh_wiz_to_date.date()),('order_id.state','=','sale')]
            if self.sh_product_id:
                domain += [('product_id','=',self.sh_product_id.id)]
            if self.sh_category_id:
                domain += [('product_id.categ_id','=',self.sh_category_id.id)]

            records = self.env['sale.order.line'].search(domain)
            # if rec.product_id.id in self.sh_product_wizard_line_ids.sh_pdt_id.id

            # self.sh_product_wizard_line_ids = [Command.create({
            #     'sh_pdt_id':rec.product_id.id,
            #     'sh_categ_id':rec.product_id.categ_id.id,
            #     'sh_qty_sold':0,
            #     'sh_unit_price':0,
            #     'sh_total_sale':0
            # })
            for rec in records:
                if rec.product_id.id not in self.sh_product_wizard_line_ids.mapped('sh_pdt_id').ids:
                    self.sh_product_wizard_line_ids = [Command.create({
                    'sh_pdt_id':rec.product_id.id,
                    'sh_categ_id':rec.product_id.categ_id.id,
                    'sh_qty_sold':0,
                    'sh_unit_price':0,
                    'sh_total_sale':0,
                    'sh_margin_rate':0,
                    'sh_total_margin':0,
                    'sh_cost_price':0
                    })]
                    # print("\n\n\n rec", rec)
                    # print("\n\n\n rec.product_id.id", rec.product_id.id)
                    # print("\n\n\n self.sh_product_wizard_line_ids.mapped('sh_pdt_id').ids", self.sh_product_wizard_line_ids.mapped('sh_pdt_id').ids)

            for record in self.sh_product_wizard_line_ids:
                for rec in records:
                    if rec.product_id.id == record.sh_pdt_id.id:
                        record.sh_qty_sold += rec.product_uom_qty
                        record.sh_total_sale += rec.price_subtotal
                record.sh_unit_price = record.sh_total_sale/record.sh_qty_sold
                record.sh_cost_price = record.sh_pdt_id.standard_price
                record.sh_total_margin = record.sh_unit_price - record.sh_cost_price 
                record.sh_margin_rate = (record.sh_total_margin*100)/record.sh_unit_price

        if self.sh_is_fsn:

            if self.sh_wiz_from_date or self.sh_wiz_to_date:
                domain += [('order_id.date_order','>=',self.sh_wiz_from_date.date()),('order_id.date_order','<=',self.sh_wiz_to_date.date()),('order_id.state','=','sale')]
            if self.sh_product_id:
                domain += [('product_id','=',self.sh_product_id.id)]
            if self.sh_category_id:
                domain += [('product_id.categ_id','=',self.sh_category_id.id)]
            # if self.sh_min_qty_rate:
            #     domain += [('product_id.qty_available','>=',)]

            records = self.env['sale.order.line'].search(domain)
                
            for rec in records:
                if rec.product_id.id not in self.sh_fsn_wizard_line_ids.mapped('sh_pdt_id').ids:
                    self.sh_fsn_wizard_line_ids = [Command.create({
                        'sh_pdt_id':rec.product_id.id,
                        'sh_categ_id':rec.product_id.categ_id.id,
                        'sh_stock_qty':rec.product_id.qty_available,
                        'sh_stock_forecast':rec.product_id.virtual_available,
                        'sh_qty_sold':0,                        
                    })]

            for record in self.sh_fsn_wizard_line_ids:
                for rec in records:
                    if rec.product_id.id == record.sh_pdt_id.id:
                        record.sh_qty_sold += rec.product_uom_qty
                
                if record.sh_qty_sold >= self.sh_min_qty_rate:
                    record.sh_sold_rate = 'fast'
                else:
                    record.sh_sold_rate = 'slow'

        if self.sh_is_patient:
            print("\n\n\n age", self.sh_age_categ)

            if self.sh_wiz_from_date or self.sh_wiz_to_date:
                domain += [('date_order','>=',self.sh_wiz_from_date.date()),('date_order','<=',self.sh_wiz_to_date.date()),('state','=','sale')]
            if self.sh_doc_id:
                domain += [('sh_doctor_id','=',self.sh_doc_id.id)]
            if self.sh_patient_id:
                domain += [('partner_id','=',self.sh_patient_id.id)]
            if self.sh_gender:
                domain += [('sh_gender','=',self.sh_gender)]
            if self.sh_age_categ:
                print("\n\n\n in age")
                if self.sh_age_categ=='child':
                    domain += [('partner_id.sh_age','>=',0),('partner_id.sh_age','<=',12)]
                elif self.sh_age_categ=='teen':
                    domain += [('partner_id.sh_age','>=',13),('partner_id.sh_age','<=',18)]
                elif self.sh_age_categ=='adult':
                    domain += [('partner_id.sh_age','>=',19),('partner_id.sh_age','<=',40)]
                elif self.sh_age_categ=='senior':
                    domain += [('partner_id.sh_age','>',40)]

            records = self.env['sale.order'].search(domain)

            self.sh_patient_wizard_line_ids = [Command.create({
                'sh_so_id':rec.id,
                'sh_so_date':rec.date_order.date(),
                'sh_patient_id':rec.partner_id.id,
                # 'sh_age':rec.sh_age,
                'sh_gender':rec.sh_gender,
                'sh_doctor_id':rec.sh_doctor_id.id,
                'sh_total_amount':rec.amount_total
            }) for rec in records]


        return {
            'type': 'ir.actions.act_window',
            'name': _('Pharmacy Reports'),   #type:ignore
            'res_model': 'sh.pharmacy.report.wizard',        
            'target': 'new',
            'view_mode': 'form',
            'view_id':self.env.ref('sh_pharmacy_management_system.sh_pharmacy_report_wizard').id,            
            'res_id':self.id                     
        }

    def export_report_action(self):
        
        self.fetch_report_action()

        if self.sh_is_cash_drawer:
            records = self.sh_cash_drawer_wizard_line_ids
        if self.sh_is_exp_date:
            records = self.sh_exp_date_wizard_line_ids
        if self.sh_is_doctor_commission:
            records = self.sh_doctor_commission_wizard_line_ids
        if self.sh_is_product_selling:
            records = self.sh_product_wizard_line_ids
        if self.sh_is_fsn:
            records = self.sh_fsn_wizard_line_ids
        if self.sh_is_patient:
            records = self.sh_patient_wizard_line_ids


        workbook = xlwt.Workbook(encoding='utf-8')
                       
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        if self.sh_is_cash_drawer:
            worksheet = workbook.add_worksheet("Cash Drawer")
        if self.sh_is_exp_date:
            worksheet = workbook.add_worksheet("Expiry Date")
        if self.sh_is_doctor_commission:
            worksheet = workbook.add_worksheet("Doctor Commission")
        if self.sh_is_product_selling:
            worksheet = workbook.add_worksheet("Product Selling")
        if self.sh_fsn_wizard_line_ids:
            worksheet = workbook.add_worksheet("FSN Report")
        if self.sh_patient_wizard_line_ids:
            worksheet = workbook.add_worksheet("Patient Report")

        # print("\n\n\n records", records)

        bold_style = workbook.add_format({'bold': True,'align': 'center','valign': 'vcenter','border': 1})
        num_format = workbook.add_format({'num_format': '#,##0.00','align': 'right','valign': 'vcenter','border': 1})
        
        if self.sh_is_cash_drawer:
            worksheet.merge_range('A1:R1', 'Cash Drawer Report', workbook.add_format({
                'bold': True,
                'font_size': 14,
                'align': 'center',
                'valign': 'vcenter'
            }))
        
        if self.sh_is_exp_date:
            worksheet.merge_range('A1:R1', 'Expiry Date Report', workbook.add_format({
                'bold': True,
                'font_size': 14,
                'align': 'center',
                'valign': 'vcenter'
            }))

        if self.sh_is_doctor_commission:
            worksheet.merge_range('A1:R1', 'Doctor Commission Report', workbook.add_format({
                'bold': True,
                'font_size': 14,
                'align': 'center',
                'valign': 'vcenter'
            }))

        if self.sh_is_product_selling:
            worksheet.merge_range('A1:R1', 'Product Selling Report', workbook.add_format({
                'bold': True,
                'font_size': 14,
                'align': 'center',
                'valign': 'vcenter'
            }))

        if self.sh_is_fsn:
            worksheet.merge_range('A1:R1', 'FSN Report', workbook.add_format({
                'bold': True,
                'font_size': 14,
                'align': 'center',
                'valign': 'vcenter'
            }))

        if self.sh_is_patient:
            worksheet.merge_range('A1:R1', 'Patient Report', workbook.add_format({
                'bold': True,
                'font_size': 14,
                'align': 'center',
                'valign': 'vcenter'
            }))

        date_range = f'From: {self.sh_wiz_from_date.strftime("%d/%m/%Y")} To: {self.sh_wiz_to_date.strftime("%d/%m/%Y")}'
        worksheet.merge_range('A2:R2', date_range, workbook.add_format({
            'font_size': 11,
            'align': 'center',
            'valign': 'vcenter'
        }))

        if self.sh_is_cash_drawer:
            header = [
                'Sr. No.', 'Date', 'Cashier','Opening Balance', 'Closing Balance', 'Cash Sale', 'Card Sale', 'UPI Sale', 'Net Cash' 
            ]
        
        if self.sh_is_exp_date:
            header = [
                'Sr. No.', 'Product', 'Lot/Sr no.','Exipry Date', 'Days Remaining', 'Quantity', 'Category' 
            ]

        if self.sh_is_doctor_commission:
            header = [
                'Sr. No.', 'Doctor', 'Patient','Sale Order', 'Date', 'Total Bill Amount', 'Commission Percentage', 'Commission Fixed Amount', 'Commission Amount' 
            ]
        
        if self.sh_is_product_selling:
            header = [
                'Sr. No.', 'Product', 'Category','Quantity Sold', 'Unit/Sale Price', 'Total Sale', 'Margin Rate(%)', 'Total Margin Amount', 'Cost Price' 
            ]

        if self.sh_is_fsn:
            header = [
                'Sr. No.', 'Product', 'Category','Quantity On Hand', 'Quantity Forecast', 'Quantity Sold', 'Sale Rate' 
            ]

        if self.sh_is_patient:
            header = [
                'Sr. No.', 'Order', 'Order Date','Patient', 'Age', 'Gender', 'Doctor', 'Amount' 
            ]

        header_format = workbook.add_format({'bold': True, 'bg_color': '#D3D3D3'})
        for col, title in enumerate(header):
            worksheet.write(2, col, title, header_format)

        col_widths = [len(title) for title in header]
        row = 3
        count = 1
        

        for rec in records:    

            if self.sh_is_cash_drawer:
                values = [
                    str(count),
                    rec.sh_date.strftime("%d/%m/%Y"),
                    rec.sh_cashier_id.name,
                    rec.sh_open_bal,
                    rec.sh_close_bal,                
                    rec.sh_cash_sale,    
                    rec.sh_card_sale,
                    rec.sh_upi_sale,
                    rec.sh_net_cash
                ]

            if self.sh_is_exp_date:
                values = [
                    str(count),
                    rec.sh_pdt_id.name,
                    rec.sh_lot_name,
                    rec.sh_exp_date.strftime("%d/%m/%Y"),
                    rec.sh_days_remaining,                
                    rec.sh_qty,    
                    rec.sh_category_id.name                    
                ]

            if self.sh_is_doctor_commission:
                values = [
                    str(count),
                    rec.sh_doctor_id.name,
                    rec.sh_patient_id.name,
                    rec.sh_so_id.name,
                    rec.sh_date.strftime("%d/%m/%Y"),                
                    rec.sh_bill_total,    
                    rec.sh_commission_percentage,
                    rec.sh_commission_fixed_amount,
                    rec.sh_com_amount                    
                ]

            if self.sh_is_product_selling:
                values = [
                    str(count),
                    rec.sh_pdt_id.name,
                    rec.sh_categ_id.name,
                    rec.sh_qty_sold,
                    rec.sh_unit_price,
                    rec.sh_total_sale,
                    rec.sh_margin_rate,
                    rec.sh_total_margin,
                    rec.sh_cost_price
                ]

            if self.sh_is_fsn:
                values = [
                    str(count),
                    rec.sh_pdt_id.name,
                    rec.sh_categ_id.name,
                    rec.sh_stock_qty,
                    rec.sh_stock_forecast,
                    rec.sh_qty_sold,
                    rec.sh_sold_rate
                ]

            if self.sh_is_patient:
                values = [
                    str(count),
                    rec.sh_so_id.name,
                    rec.sh_so_date,
                    rec.sh_patient_id.name,
                    rec.sh_age,
                    rec.sh_gender,
                    rec.sh_doctor_id.name,
                    rec.sh_total_amount
                ]
                
                # Write values and update column widths
            for col, val in enumerate(values):
                worksheet.write(row, col, val)
                col_widths[col] = max(col_widths[col], len(str(val)))

            row += 1
            count += 1

        # Apply final column widths
        for col, width in enumerate(col_widths):
            worksheet.set_column(col, col, width + 2)  # +2 for padding

        fp = io.BytesIO()
        workbook.close()
        output.seek(0)
        xlsx_data = base64.b64encode(output.read())
        IrAttachment = self.env['ir.attachment']
        
        if self.sh_is_cash_drawer:
            attachment_vals = {
            'name': 'Cash Drawer Report.xls',
            'res_model': 'ir.ui.view',
            'type': 'binary',
            'datas': xlsx_data,
            'public': True,
            }
        
            fp.close()

            attachment = IrAttachment.search([('name', '=',
                    'Cash Drawer Report.xls'), ('type', '=', 'binary'),
                    ('res_model', '=', 'ir.ui.view')], limit=1)

        if self.sh_is_exp_date:
            attachment_vals = {
            'name': 'Expiry Date Report.xls',
            'res_model': 'ir.ui.view',
            'type': 'binary',
            'datas': xlsx_data,
            'public': True,
            }
        
            fp.close()

            attachment = IrAttachment.search([('name', '=',
                    'Expiry Date Report.xls'), ('type', '=', 'binary'),
                    ('res_model', '=', 'ir.ui.view')], limit=1)

        if self.sh_is_doctor_commission:
            attachment_vals = {
            'name': 'Doctor Commission Report.xls',
            'res_model': 'ir.ui.view',
            'type': 'binary',
            'datas': xlsx_data,
            'public': True,
            }
        
            fp.close()

            attachment = IrAttachment.search([('name', '=',
                    'Doctor Commission Report.xls'), ('type', '=', 'binary'),
                    ('res_model', '=', 'ir.ui.view')], limit=1)

        if self.sh_is_product_selling:
            attachment_vals = {
            'name': 'Product Selling Report.xls',
            'res_model': 'ir.ui.view',
            'type': 'binary',
            'datas': xlsx_data,
            'public': True,
            }
        
            fp.close()

            attachment = IrAttachment.search([('name', '=',
                    'Product Selling Report.xls'), ('type', '=', 'binary'),
                    ('res_model', '=', 'ir.ui.view')], limit=1)

        if self.sh_is_fsn:
            attachment_vals = {
            'name': 'FSN Report.xls',
            'res_model': 'ir.ui.view',
            'type': 'binary',
            'datas': xlsx_data,
            'public': True,
            }
        
            fp.close()

            attachment = IrAttachment.search([('name', '=',
                    'FSN Report.xls'), ('type', '=', 'binary'),
                    ('res_model', '=', 'ir.ui.view')], limit=1)

        if self.sh_is_patient:
            attachment_vals = {
            'name': 'Patient Report.xls',
            'res_model': 'ir.ui.view',
            'type': 'binary',
            'datas': xlsx_data,
            'public': True,
            }
        
            fp.close()

            attachment = IrAttachment.search([('name', '=',
                    'Patient Report.xls'), ('type', '=', 'binary'),
                    ('res_model', '=', 'ir.ui.view')], limit=1)

        if attachment:
            attachment.write(attachment_vals)
        else:
            attachment = \
                IrAttachment.create(attachment_vals)
        if not attachment:
            raise UserError('There is no attachments...')

        url = '/web/content/' + str(attachment.id) \
            + '?download=true'
        return {'type': 'ir.actions.act_url', 'url': url,
                'target': 'new'}

    
    def export_pdf_action(self):
        self.fetch_report_action()

        if self.sh_is_cash_drawer:
            return self.env.ref('sh_pharmacy_management_system.action_report_sh_cash_drawer').report_action(self)
        if self.sh_is_exp_date:
            return self.env.ref('sh_pharmacy_management_system.action_report_sh_expiry_date').report_action(self)
        if self.sh_is_doctor_commission:
            return self.env.ref('sh_pharmacy_management_system.action_report_sh_doctor_commission').report_action(self)            
        if self.sh_is_product_selling:
            return self.env.ref('sh_pharmacy_management_system.action_report_sh_product_selling').report_action(self)
        if self.sh_is_fsn:
            return self.env.ref('sh_pharmacy_management_system.action_report_sh_fsn').report_action(self)
        if self.sh_is_patient:
            return self.env.ref('sh_pharmacy_management_system.action_report_sh_patient').report_action(self)

        
        

'''
    def print_xls_report(self):
        workbook = xlwt.Workbook(encoding='utf-8')
        invoice_domain = [('move_type', '=', 'out_invoice'),('invoice_date', '>=', self.start_date),('invoice_date', '<=', self.end_date)]
        invoices = self.env['account.move'].search(invoice_domain)
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet("Invoices")

        bold_style = workbook.add_format({'bold': True,'align': 'center','valign': 'vcenter','border': 1})
        num_format = workbook.add_format({'num_format': '#,##0.00','align': 'right','valign': 'vcenter','border': 1})
        worksheet.merge_range('A1:R1', 'Invoice Payment Report', workbook.add_format({
            'bold': True,
            'font_size': 14,
            'align': 'center',
            'valign': 'vcenter'
        }))
        date_range = f'From: {self.start_date.strftime("%d/%m/%Y")} To: {self.end_date.strftime("%d/%m/%Y")}'
        worksheet.merge_range('A2:R2', date_range, workbook.add_format({
            'font_size': 11,
            'align': 'center',
            'valign': 'vcenter'
        }))

        header = [
            'SR. NO.', 'INVOICE NUMBER', 'DATE', 'GSTIN', 'AMOUNT', 'CURRENCY', 'EXCHANGE RATE',
            'AMOUNT (RS.)', 'NAME OF PARTY', 'CITY / COUNTRY', 'STATE', 'HSN', 'RATE',
            'IGST', 'CGST', 'SGST', 'TOTAL', 'PAID BY'
        ]
        header_format = workbook.add_format({'bold': True, 'bg_color': '#D3D3D3'})
        for col, title in enumerate(header):
            worksheet.write(2, col, title, header_format)

        row = 3
        count = 1
        col_widths = [len(title) for title in header]
        total_amount = total_amount_rs = total_igst = total_cgst = total_sgst = total_invoice_total = 0.0
        for inv in invoices:

            if inv.state == 'cancel':
                values = [
                    str(count),
                    inv.name,
                    '', '', '', '', '',
                    '-',
                    'CANCELLED INVOICE',
                    '', '', '', '', '', '', '', '-', ''
                ]
            else:
                exchange_rate = self.fetch_currency_rate(inv.invoice_date,inv.currency_id)
                hsn = inv.invoice_line_ids[0].product_id.l10n_in_hsn_code if inv.invoice_line_ids else ''
                rate = '18%' if inv.partner_id.state_id.code == 'GJ' else '0%'
                payment_jornal = self.env['account.payment'].search([('ref', '=', inv.name)], limit=1)

                country_code = inv.partner_id.country_id.code or ""
                country_name = inv.partner_id.country_id.name or ""
                state_name = inv.partner_id.state_id.name or ''
                city_name = inv.partner_id.city or ""
                city_or_country = (city_name if country_code == 'IN' else country_name)
                state = state_name if country_code and country_code == 'IN' else 'Outside Inda' if country_code else ''

                igst = cgst = sgst = 0.0

                for line in inv.tax_totals.get('groups_by_subtotal', {}).get('Untaxed Amount', []):
                    amount = line.get('tax_group_amount', 0.0)
                    group = line.get('tax_group_name', '')

                    if group == 'IGST':
                        igst += amount
                    elif group == 'CGST':
                        cgst += amount
                    elif group == 'SGST':
                        sgst += amount

                total_amount += inv.amount_total
                total_amount_rs += inv.amount_total_signed
                total_igst += igst
                total_cgst += cgst
                total_sgst += sgst
                total_invoice_total += inv.amount_tax_signed

                values = [
                    str(count),
                    inv.name,
                    inv.invoice_date.strftime('%m/%d/%Y') if inv.invoice_date else '',
                    inv.partner_id.vat or '',
                    str(inv.amount_total),
                    inv.currency_id.name,
                    round(exchange_rate,2) ,
                    str(inv.amount_total_signed),
                    inv.partner_id.name,
                    city_or_country,
                    state,
                    hsn or '',
                    rate,
                    igst, cgst, sgst, str(inv.amount_tax_signed),
                    payment_jornal.journal_id.name or 'N/A'
                ]

            # Write values and update column widths
            for col, val in enumerate(values):
                worksheet.write(row, col, val)
                col_widths[col] = max(col_widths[col], len(str(val)))

            row += 1
            count += 1


        # Apply final column widths
        for col, width in enumerate(col_widths):
            worksheet.set_column(col, col, width + 2)  # +2 for padding

        fp = io.BytesIO()
        workbook.close()
        output.seek(0)
        xlsx_data = base64.b64encode(output.read())
        IrAttachment = self.env['ir.attachment']
        attachment_vals = {
            'name': 'Invoice Payment Report.xls',
            'res_model': 'ir.ui.view',
            'type': 'binary',
            'datas': xlsx_data,
            'public': True,
            }
        fp.close()

        attachment = IrAttachment.search([('name', '=',
                'Invoice Payment Report.xls'), ('type', '=', 'binary'),
                ('res_model', '=', 'ir.ui.view')], limit=1)
        if attachment:
            attachment.write(attachment_vals)
        else:
            attachment = \
                IrAttachment.create(attachment_vals)
        if not attachment:
            raise UserError('There is no attachments...')

        url = '/web/content/' + str(attachment.id) \
            + '?download=true'
        return {'type': 'ir.actions.act_url', 'url': url,
                'target': 'new'}
'''        