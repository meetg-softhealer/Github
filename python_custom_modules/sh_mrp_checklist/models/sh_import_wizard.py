# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,_ #type:ignore
from odoo.exceptions import UserError #type:ignore
import base64
import csv
import io
import xlrd 

class ImportWizard(models.TransientModel):
    _name = "import.wizard"

    import_file_type = fields.Selection(selection=[('csv','CSV'),('xlsx','Excel')])
    company_id = fields.Many2one("res.company", string="Company")
    file = fields.Binary(string="File")

    def process_file(self):
            print("\n\n\n\n\n=====type",self.import_file_type)

            if self.file:
                if self.import_file_type == "csv":
                    self._process_csv()
                elif self.import_file_type == "xlsx":
                    self._process_excel()
                else:
                    raise UserError("Unsupported file format. Please upload CSV or Excel file.")
            else:
                raise UserError("Please enter the file")
    
    def _process_csv(self):
        decoded_file = base64.b64decode(self.file)

        try:
            file_io = io.StringIO(decoded_file.decode("utf-8"))
            reader = csv.DictReader(file_io)
        except Exception as e:
            raise UserError(f"Failed to read CSV content: {str(e)}")

        for row in reader:
            # Example: Create a partner
            print('\n\n\n-----row.get("name")------->',row.get("Name"))
            self.env["manufacturing.checklist"].create(
                {
                    "name": row.get("Name"),
                    "description": row.get("Description"),
                    "company_id": self.company_id.id,
                }
            )

    def _process_excel(self):
        decoded_file = base64.b64decode(self.file)
        if self.import_file_type == "xlsx":
            workbook = xlrd.open_workbook(file_contents=decoded_file)
            sheet = workbook.sheet_by_index(0)
            headers = sheet.row_values(0)

            for row_idx in range(1, sheet.nrows):
                row = sheet.row_values(row_idx)
                data = dict(zip(headers, row))
                print(f"Row {row_idx}: {row}")
    
                self.env["manufacturing.checklist"].create(
                    {
                        "name": data.get("Name"),
                        "description": data.get("Description"),
                        "company_id": self.company_id.id,
                    }
                )