# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,_ #type:ignore
from odoo.exceptions import UserError #type:ignore
import xlwt #type:ignore
import io
import xlsxwriter #type:ignore
import base64
from datetime import datetime
from dateutil.relativedelta import relativedelta

class ShCashDrawerReportWizard(models.TransientModel):
    _name = "sh.cash.drawer.report.wizard"

    sh_wiz_from_date = fields.Datetime("From:", default=datetime.today()-relativedelta(months=1))    

    sh_wiz_to_date = fields.Datetime("To:", default=datetime.today())

    sh_wiz_cashier_id = fields.Many2one("res.users", string="Cashier")

    def export_report_action(self):
        workbook = xlwt.Workbook(encoding='utf-8')
        if not self.sh_wiz_from_date or not self.sh_wiz_to_date:
            raise UserError("Enter From and To date fields to generate reports!!!")

        if self.sh_wiz_from_date and self.sh_wiz_to_date and self.sh_wiz_cashier_id:
            records = self.env['pos.session'].search([('start_at','>=',self.sh_wiz_from_date),('stop_at','<=',self.sh_wiz_to_date),('user_id','=',self.sh_wiz_cashier_id.id)])
            
        # elif self.sh_wiz_from_date and self.sh_wiz_to_date:            
        #     records = self.env['pos.session'].sudo().search([('start_at','>=',self.sh_wiz_from_date),('stop_at','<=',self.sh_wiz_to_date)])
        #     print("\n\n\n recs", records)
        #     print("domian",[('start_at','>=',self.sh_wiz_from_date),('stop_at','<=',self.sh_wiz_to_date)])
        # elif self.sh_wiz_from_date and self.sh_wiz_cashier_id:
        #     records = self.env['pos.session'].search([('start_at','>=',self.sh_wiz_from_date),('user_id','=',self.sh_wiz_cashier_id.id)])
            
        # elif self.sh_wiz_to_date and self.sh_wiz_cashier_id:
        #     records = self.env['pos.session'].search([('stop_at','<=',self.sh_wiz_from_date),('user_id','=',self.sh_wiz_cashier_id.id)])
        
        # elif self.sh_wiz_from_date:
        #     records = self.env['pos.session'].search([('start_at','>=',self.sh_wiz_from_date)])    
       
        # elif self.sh_wiz_to_date:
        #     records = self.env['pos.session'].search([('stop_at','<=',self.sh_wiz_from_date)])
        
        # elif self.sh_wiz_cashier_id:
        #     records = self.env['pos.session'].search([('user_id','=',self.sh_wiz_cashier_id.id)])


        
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
            print("In Rec Loop", rec)        
            cash_sale = rec.env['pos.payment'].search([('payment_method_id.name','=','Cash'),('payment_date','>=',rec.start_at),('payment_date','<=',rec.stop_at)])
            cash_sale_total = 0
            for item in cash_sale:
                cash_sale_total += item.amount
                print("\n\n Item",item.amount)
            print("\n\n Cash Total",cash_sale_total)

            card_sale = rec.env['pos.payment'].search([('payment_method_id.name','=','Card'),('payment_date','>=',rec.start_at),('payment_date','<=',rec.stop_at)])
            card_sale_total = 0
            for item in card_sale:
                card_sale_total += item.amount
                print("\n\n Item",item.amount)
            print("\n\n Card Total",card_sale_total)

            upi_sale = rec.env['pos.payment'].search([('payment_method_id.name','=','UPI'),('payment_date','>=',rec.start_at),('payment_date','<=',rec.stop_at)])
            upi_sale_total = 0
            for item in upi_sale:
                upi_sale_total += item.amount
                

            values = [
                str(count),
                rec.start_at.strftime("%d/%m/%Y"),
                rec.user_id.name,
                rec.cash_register_balance_start,
                rec.cash_register_balance_end_real,                
                cash_sale_total,    
                card_sale_total,
                upi_sale_total,
                rec.cash_register_balance_end_real
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