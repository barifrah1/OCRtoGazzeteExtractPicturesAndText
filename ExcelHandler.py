from Consts import EXCEL_FILE,SHEET_NAME
import pandas as pd

class ExcelHandler:
    def __init__(self):
        self.excel = pd.read_excel(EXCEL_FILE,SHEET_NAME,engine='openpyxl')
    
    # get- date in format d.m.yyyy, returns all rows with this date in Publication dd//mm/yyyy column 
    def get_rows_from_date(self,date):
        try:
            lines_from_date = self.excel[self.excel["Publication dd//mm/yyyy"]=='OG '+date]
            return lines_from_date
        except Exception as e:
            print("Error: cannot extract rows from excel, given date or excel path is is not valid")
            raise e
    def get_row_by_application_number(self,date,num):
        self.rows = self.get_rows_from_date(date)
        return self.rows[self.rows["Application No."]==str(num)]
    def get_class_by_application_number(self,date,num):
        self.rows = self.get_rows_from_date(date)
        return int(self.rows[self.rows["Application No."]==num]["Class No."].values[0])

    
      