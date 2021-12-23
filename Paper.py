from Consts import PAPERS_FOLDER, STATUS_FOLDER
import pandas as pd
from TextTrademark import TextTrademark
from ImageTrademark import ImageTrademark
import Utils
import os
from HtmlHandler import HtmlHandler
FIle_NAME_INDEX = 0


class Paper:
    def __init__(self, file, excel):
        try:
            self.original_file_name = file
            self.file_name = file.split('.')[FIle_NAME_INDEX]
            self.paper_path = PAPERS_FOLDER+'/'+file
            self.status_path = STATUS_FOLDER+'/'+self.file_name+'.txt'
            self.paper_date = Utils.convert_file_date(self.file_name)
            self.rows_for_date = excel.get_rows_from_date(self.paper_date)
            self.number_of_rows = len(self.rows_for_date.values.tolist())
            self.excel = excel
            Utils.create_folder_if_not_exist(STATUS_FOLDER)
            # if current file havent been analyzed yet ,extract already finished on empty_mode (no 1's in already done dictionary)
            is_status_file_path_exists = os.path.exists(
                STATUS_FOLDER+'/'+self.file_name+'.txt')
            self.already_done, self.romans_done = self.get_already_finished(
                excel, empty_mode=not is_status_file_path_exists)
            with open(self.paper_path, encoding="utf8") as fp:
                self.html = HtmlHandler(fp)
            self.trademarks = []
        except Exception as e:
            print(
                f'failed to create paper object and process file: {file} eror is: {e}')
            raise Exception(e)

    def extract(self):
        d = {}
        is_exist = os.path.exists(
            './'+PAPERS_FOLDER+'/'+self.file_name)
        if(is_exist == False):
            os.chdir(PAPERS_FOLDER)
            os.mkdir(self.file_name)
            os.chdir('..')
        for i in range(1, self.number_of_rows+1):
            if(i not in self.romans_done):
                try:
                    d[i] = self.extract_trademark_by_roman_number(i)
                except Exception as e:
                    print("number ", i, "failed due to: ", e,)
            else:
                print(f"{i} already done")
        print(d)

    # get excel file and paper object, return a dictionary with 1 for application numbers that have been already extracted and 0 for the rest
    # based on excel tuples
    # return also all roman numbers found

    def get_already_finished(self, excel, empty_mode=False):
        romans = []
        excel_rows = excel.excel
        rows = excel_rows[excel_rows["Publication dd//mm/yyyy"]
                          == 'OG '+self.paper_date]
        application_numbers = rows["Application No."].values.tolist()
        done = {int(key): 0 for key in application_numbers}
        if(empty_mode == False):
            with open(self.status_path, 'r') as f:
                line = f.readline()
                while(line != ''):
                    number = int(line.split('-')[0])
                    roman = int(line.split('-')[1])
                    done[number] = 1
                    romans.append(roman)
                    line = f.readline()
            return done, romans
        else:
            return done, []

    def extract_trademark_by_roman_number(self, i):
        application_number_tag = self.html.find_application_number_tag(
            i)
        if(application_number_tag is not None):
            # future developmentnumbers = Utils.parse_numbers_from_string(application_number_tag,self.rows_for_date)
            keys_not_found_yet = Utils.get_only_zero_value_from_dict(
                self.already_done)
            # check for all app_number not used yet from this date if it appears in application tag
            app_num_and_class_flag, application_number, class_number = self.check_if_class_and_app_num_in_tag(
                keys_not_found_yet, application_number_tag)
            if(app_num_and_class_flag):
                # if true, we can get all the data for application num from excel
                trademark_data = self.excel.get_trademark_data_by_application_number(
                    self.paper_date, application_number)
                trademark_type = trademark_data["type"]
                if(trademark_type == "Text"):
                    word_to_search = trademark_data["Sign"]
                    text_tag = self.html.extract_text_tag(
                        application_number_tag, word_to_search=word_to_search)
                    # if it not image
                    trademark = TextTrademark(
                        i, text_tag, application_number=trademark_data["application_number"], class_number=trademark_data[
                            "'class_number'"], initial_no=trademark_data["Initial No."], date_published=trademark_data["date_published"],
                        applicant=trademark_data["applicant"], local_agent=trademark_data[
                            "local_agent"], date_applicated=trademark_data["date_applicated"],
                    )
                if(trademark_type == 'Image'):
                    image_tag = self.html.find_image_tag(
                        application_number_tag)
                    trademark = ImageTrademark(
                        i, image_tag, application_number=trademark_data["application_number"], class_number=trademark_data[
                            "'class_number'"], initial_no=trademark_data["Initial No."], date_published=trademark_data["date_published"],
                        applicant=trademark_data["applicant"], local_agent=trademark_data[
                            "local_agent"], date_applicated=trademark_data["date_applicated"],
                    )
                else:
                    raise Exception(
                        "trademark type is not defined text/image")
                trademark.save_trademark()
                self.trademarks.append(trademark)
        else:
            return None

    def check_if_class_and_app_num_in_tag(self, keys_not_found_yet, application_number_tag):
        app_num_and_class_flag = False
        for app_num in keys_not_found_yet:
            if(Utils.check_if_num_in_string(app_num, application_number_tag)):
                class_num = self.excel.get_class_by_application_number(
                    self.paper_date, app_num)
                if(Utils.check_if_num_in_string(class_num, application_number_tag)):
                    # both class and application number havent been found yet
                    app_num_and_class_flag = True
                    application_number = app_num
                    class_number = class_num
                    return True, application_number, class_number
        return None, -1, -1
