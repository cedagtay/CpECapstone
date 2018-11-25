from openpyxl import *

class Database():
    def __init__(self):
        try:
            self.wb = load_workbook('./data/excel.xlsx')
        except:
            self.wb = Workbook()
            sheet = self.wb.active
            # resize the width of columns in 
            # excel spreadsheet 
            sheet.column_dimensions['A'].width = 30
            sheet.column_dimensions['B'].width = 10
            sheet.column_dimensions['C'].width = 10
            sheet.column_dimensions['D'].width = 20
            sheet.column_dimensions['E'].width = 20
            sheet.column_dimensions['F'].width = 40
            sheet.column_dimensions['G'].width = 50
            
            # write given data to an excel spreadsheet 
            # at particular location 
            sheet.cell(row=1, column=1).value = "Name"
            sheet.cell(row=1, column=2).value = "Course"
            sheet.cell(row=1, column=3).value = "Semester"
            sheet.cell(row=1, column=4).value = "Form Number"
            sheet.cell(row=1, column=5).value = "Contact Number"
            sheet.cell(row=1, column=6).value = "Email id"
            sheet.cell(row=1, column=7).value = "Address"
            self.wb.save('./data/excel.xlsx')
            
    def insert_data(self, name, course, sem, form_no, contact_no, email_id, address):
        sheet = self.wb.active
        current_row = sheet.max_row
        sheet.cell(row=current_row + 1, column=1).value = name
        sheet.cell(row=current_row + 1, column=2).value = course 
        sheet.cell(row=current_row + 1, column=3).value = sem
        sheet.cell(row=current_row + 1, column=4).value = form_no 
        sheet.cell(row=current_row + 1, column=5).value = contact_no 
        sheet.cell(row=current_row + 1, column=6).value = email_id
        sheet.cell(row=current_row + 1, column=7).value = address
        self.wb.save('./data/excel.xlsx')
        
