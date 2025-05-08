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


    sh_wiz_from_date = fields.Datetime("From:", default=datetime.today()-relativedelta(months=1))    

    sh_wiz_to_date = fields.Datetime("To:", default=datetime.today())

    # Cash Drawer Fields
    sh_wiz_cashier_id = fields.Many2one("res.users", string="Cashier")
    sh_cash_drawer_wizard_line_ids = fields.Many2many("sh.cash.drawer.wizard.line")

    # Expiry Date Fields
    sh_product_id = fields.Many2one("product.product", string="Product:")
    sh_category_id = fields.Many2one("product.category", string="Category: ")
    sh_remaining_days = fields.Integer(string="Remaining Days:")
    sh_lot_id = fields.Many2one("stock.lot", string="Batch Number")
    sh_exp_date_wizard_line_ids = fields.Many2many("sh.exp.date.wizard.line") 

    def fetch_report_action(self):
        self.sh_is_fetch = True
        
        if self.sh_is_cash_drawer:

            date_domain = [('start_at','>=',self.sh_wiz_from_date),('stop_at','<=',self.sh_wiz_to_date)]
            if not self.sh_wiz_from_date or not self.sh_wiz_to_date:
                    raise UserError("Enter From and To date fields to generate reports!!!")
            
            if self.sh_wiz_from_date and self.sh_wiz_to_date and self.sh_wiz_cashier_id:
                records = self.env['pos.session'].search([('user_id','=',self.sh_wiz_cashier_id.id)]+date_domain)
                
            elif self.sh_wiz_from_date and self.sh_wiz_to_date:            
                records = self.env['pos.session'].sudo().search([date_domain])
                print("\n\n\n recs", records)

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
                rec.sh_net_cash = rec.sh_close_bal
        
        if self.sh_is_exp_date:
            domain = []

            if self.sh_wiz_from_date:
                domain += [('expiration_date','>=',self.sh_wiz_from_date)]
            if self.sh_wiz_to_date:
                domain += [('expiration_date','<=',self.sh_wiz_to_date)]
            if self.sh_product_id:
                domain += [('product_id','=',self.sh_product_id.id)]
            if self.sh_category_id:
                domain += [('product_id.categ_id','=',self.sh_product_id.categ_id.id)]
            if self.sh_remaining_days:
                domain += [('sh_days_remaining','<=',self.sh_remaining_days)]
            if self.sh_lot_id:
                domain += [('name','=',self.sh_lot_id.name)]

            records = self.env['stock.lot'].search(domain)

            self.sh_exp_date_wizard_line_ids = [Command.create({
                                                'sh_pdt_id':rec.product_id.id,
                                                'sh_lot_name':rec.name,
                                                'sh_exp_date':rec.expiration_date,
                                                'sh_qty':rec.product_qty,                                            
                                                'sh_category_id':rec.product_id.categ_id.id
            }) for rec in records]

            for rec in self.sh_exp_date_wizard_line_ids:
                rec.sh_days_remaining = int(rec.sh_exp_date - datetime.now())
         
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
        if self.sh_is_cash_drawer:
            records = self.sh_cash_drawer_wizard_line_ids
        
        workbook = xlwt.Workbook(encoding='utf-8')
                       
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet("Cash Drawer")
        # print("\n\n\n records", records)

        bold_style = workbook.add_format({'bold': True,'align': 'center','valign': 'vcenter','border': 1})
        num_format = workbook.add_format({'num_format': '#,##0.00','align': 'right','valign': 'vcenter','border': 1})

        worksheet.merge_range('A1:R1', 'Cash Drawer Report', workbook.add_format({
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

        header = [
            'Sr. No.', 'Date', 'Cashier','Opening Balance', 'Closing Balance', 'Cash Sale', 'Card Sale', 'UPI Sale', 'Net Cash' 
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
                    rec.sh_date,
                    rec.sh_cashier_id.name,
                    rec.sh_open_bal,
                    rec.sh_close_bal,                
                    rec.sh_cash_sale,    
                    rec.sh_card_sale,
                    rec.sh_upi_sale,
                    rec.sh_net_cash
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