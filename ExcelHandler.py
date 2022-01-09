from Consts import EXCEL_FILE, SHEET_NAME
import pandas as pd
import Utils


class ExcelHandler:
    def __init__(self):
        self.excel = pd.read_excel(EXCEL_FILE, SHEET_NAME, engine='openpyxl')

    # get- date in format d.m.yyyy, returns all rows with this date in Publication dd//mm/yyyy column
    def get_rows_from_date(self, date):
        try:
            lines_from_date = self.excel[self.excel["Publication dd//mm/yyyy"] == 'OG '+date]
            return lines_from_date
        except Exception as e:
            print(
                "Error: cannot extract rows from excel, given date or excel path is is not valid")
            raise e

    def get_row_by_application_number(self, date, num):
        self.rows = self.get_rows_from_date(date)
        return self.rows[self.rows["Application No."] == int(num)]

    def get_class_by_application_number(self, date, num):
        self.rows = self.get_rows_from_date(date)
        return int(self.rows[self.rows["Application No."] == num]["Class No."].values[0])

    def get_trademark_data_by_application_number(self, date, num):
        row = self.get_row_by_application_number(date, num)
        if(row.shape[0] == 1):
            di = {'application_number': str(int(row["Application No."].values[0])),
                  'class_number': row["Class No."].values[0],
                  'type': Utils.parse_trademark_type(row),
                  'initial_no': row["Initial No."].values[0],
                  'date_published': date,
                  'applicant': row["Applicant"].values[0],
                  'local_agent': row["Local Agent"].values[0],
                  'date_applicated': row["Date of Application"].values[0],
                  'sign': row["Sign"].to_list()[0]
                  }
        else:
            raise Exception(f"more than one row were found for app_num {num}",)
        return di

    def is_trademark_type_text(self, app_num):
        row = self.rows[self.rows["Application No."] == app_num]
        return ('Word' in str(row['Symbol Contents']) and str(row['Sign']) != '')

    def get_all_images_app_nums(self, date):
        self.rows = self.get_rows_from_date(date)
        app_nums = []
        for index, row in self.rows.iterrows():
            if('Word' in str(row['Symbol Contents']) and 'Symbol' in str(row['Symbol Contents'])):
                type = 'Image'
            elif(('Word' in str(row['Symbol Contents']) and str(row['Sign']) != '')):
                type = 'Text'
            else:
                type = 'Image'

            if(type == 'Image'):
                app_nums.append(int((row['Application No.'])))
        return app_nums

    def get_all_text_app_nums(self, date):
        self.rows = self.get_rows_from_date(date)
        app_nums = []
        for index, row in self.rows.iterrows():
            if('Word' in str(row['Symbol Contents']) and 'Symbol' in str(row['Symbol Contents'])):
                type = 'Image'
            elif(('Word' in str(row['Symbol Contents']) and str(row['Sign']) != '')):
                type = 'Text'
            else:
                type = 'Image'

            if(type == 'Text'):
                app_nums.append(int((row['Application No.'])))
        return app_nums
