# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,_,Command #type:ignore
from odoo.exceptions import UserError #type:ignore
import xlwt #type:ignore
import io
import xlsxwriter #type:ignore
import base64


class ShShiftWizardReport(models.TransientModel):
    _name = "sh.shift.wizard.report"

    sh_bool = fields.Boolean()    
    sh_from_date = fields.Date("From Date", required=True)
    sh_to_date = fields.Date("To Date", required=True)
    sh_employee_id = fields.Many2one("hr.employee", string="Employee", required=True)
    sh_shift_schedule_id = fields.Many2one("resource.calendar", string="Shift Schedule")    
    sh_shift_type_id = fields.Many2one("sh.shift.type", string="Shift Type")
    sh_shift_wizard_line_ids = fields.Many2many("sh.shift.report.wizard.line", string="")    
    
    def sh_view_report_action(self):
        self.sh_bool = True

        print("\n\n\n in views")

        domain = [('sh_date','>=',self.sh_from_date),('sh_date','<=',self.sh_to_date)]
        
        if self.sh_employee_id:
            sh_emp_list = [self.sh_employee_id.id]
            domain += [('sh_shift_allocation_id.sh_employee_ids','in', sh_emp_list)]
        if self.sh_shift_schedule_id:
            domain += [('sh_shift_allocation_id.sh_resource_calendar_id','=', self.sh_shift_schedule_id.id)]
        if self.sh_shift_type_id:
            domain += [('sh_shift_allocation_id.sh_shift_type_id','=',self.sh_shift_type_id.id)]        
        
        records = self.env['sh.scheduled.info'].search(domain)

        self.sh_shift_wizard_line_ids = [Command.create({
            'sh_employee_id':self.sh_employee_id.id,
            'sh_shift_schedule_id':record.sh_shift_allocation_id.sh_resource_calendar_id.id,
            'sh_date':record.sh_date,
            'sh_week_day':record.sh_dayofweek,
            'sh_shift_type_id':record.sh_shift_allocation_id.sh_shift_type_id.id,
            'sh_working_hours':record.sh_shift_allocation_id.sh_working_hours
        }) for record in records]

        return {
            'type': 'ir.actions.act_window',
            'name': _('Shift Reports'),   #type:ignore
            'res_model': 'sh.shift.wizard.report',        
            'target': 'new',
            'view_mode': 'form',
            'view_id':self.env.ref('sh_shift_management.sh_shift_wizard_report_view_form').id,            
            'res_id':self.id                     
        }


    def sh_print_pdf_report_action(self):
        self.sh_view_report_action()

        return self.env.ref('sh_shift_management.action_report_sh_shift').report_action(self)

    def sh_print_excel_report_action(self):   
        self.sh_view_report_action()
        records = self.sh_shift_wizard_line_ids
        workbook = xlwt.Workbook(encoding='utf-8')       

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet("Shift Reports")

        bold_style = workbook.add_format({'bold': True,'align': 'center','valign': 'vcenter','border': 1})
        num_format = workbook.add_format({'num_format': '#,##0.00','align': 'right','valign': 'vcenter','border': 1})
        worksheet.merge_range('A1:R1', 'Shift Reports', workbook.add_format({
            'bold': True,
            'font_size': 14,
            'align': 'center',
            'valign': 'vcenter'
        }))
        date_range = f'From: {self.sh_from_date.strftime("%d/%m/%Y")} To: {self.sh_to_date.strftime("%d/%m/%Y")}'
        worksheet.merge_range('A2:R2', date_range, workbook.add_format({
            'font_size': 11,
            'align': 'center',
            'valign': 'vcenter'
        }))

        header = [
            'Sr. No.', 'Employees', 'Shift Schedule', 'Date', 'Weekday', 'Shift Type', 'Working Hours'
            ]
        header_format = workbook.add_format({'bold': True, 'bg_color': '#D3D3D3'})
        for col, title in enumerate(header):
            worksheet.write(2, col, title, header_format)

        row = 3
        count = 1
        col_widths = [len(title) for title in header]
        
        for rec in records:
            values = [
                str(count),
                rec.sh_employee_id.name,
                rec.sh_shift_schedule_id.name,
                rec.sh_date,
                rec.sh_week_day,
                rec.sh_shift_type_id.name,
                rec.sh_working_hours
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
            'name': 'Shift Report.xls',
            'res_model': 'ir.ui.view',
            'type': 'binary',
            'datas': xlsx_data,
            'public': True,
            }
        fp.close()

        attachment = IrAttachment.search([('name', '=',
                'Shift Report.xls'), ('type', '=', 'binary'),
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
