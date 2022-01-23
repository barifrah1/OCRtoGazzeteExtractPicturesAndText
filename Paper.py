from shutil import rmtree
from Consts import PAPERS_FOLDER, STATUS_FOLDER, PICKLES_FOLDER, XML_FOLDER
import pickle
from StatusHandler import StatusHandler
from TextHandler import TextHandler
from TextTrademark import TextTrademark
from ImageTrademark import ImageTrademark
from ImageTrademarkXML import ImageTrademarkXML
import Utils
import os
from HtmlHandler import HtmlHandler
from XMLHandler import XMLHandler
FIle_NAME_INDEX = 0
NOT_FOUND = 0


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
            self.status_handler = StatusHandler(self.file_name)
            self.xml = XMLHandler(self.file_name, self.rows_for_date)
            Utils.create_folder_if_not_exist(STATUS_FOLDER)
            # if current file havent been analyzed yet ,extract already finished on empty_mode (no 1's in already done dictionary)
            is_status_file_path_exists = os.path.exists(
                STATUS_FOLDER+'/'+self.file_name+'.txt')
            self.already_done, self.romans_done = self.get_already_finished(
                excel, empty_mode=not is_status_file_path_exists)
            # with open(self.paper_path, encoding="utf8") as fp:
            #     self.html = HtmlHandler(fp)
            self.trademarks = []
            self.images_app_nums_to_search = []
        except Exception as e:
            print(
                f'failed to create paper object and process file: {file} eror is: {e}')
            raise Exception(e)

    def extract(self, verification_level=1):
        d = {}
        Utils.create_folder_if_not_exist('./'+PAPERS_FOLDER+'/'+self.file_name)
        app_nums_left = []
        images_rows = Utils.get_only_zero_value_from_dict(self.already_done)
        for app_num in images_rows:
            if(self.already_done[app_num] == 0):
                app_nums_left.append(app_num)
        if(len(app_nums_left) > 0):
            self.images_app_nums_to_search = app_nums_left
            self.extract_image_trademarks(
                verification_level=verification_level)
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
                    if(line.split('-')[1].isdigit() == True):
                        roman = int(line.split('-')[1])
                    else:
                        roman = 'x'
                    done[number] = 1
                    if(roman != 'x'):
                        romans.append(roman)
                    line = f.readline()
            return done, romans
        else:
            return done, []

    def extract_trademark(self, i, verification_level=1, application_tag=None):
        if(application_tag == None):
            try:
                application_number_tag = self.html.find_application_number_tag(
                    i, verification_level=verification_level)
            except:
                raise Exception(
                    f"Couldnt found application_number_tag for {i}")
        else:
            application_number_tag = application_tag
        if(application_number_tag is not None):
            keys_not_found_yet = Utils.get_only_zero_value_from_dict(
                self.already_done)
            # check for all app_number not used yet from this date if it appears in application tag
            if(verification_level == 1):
                app_num_and_class_flag, application_number, class_number = self.check_if_class_and_app_num_in_tag(
                    keys_not_found_yet, application_number_tag)
            else:
                app_num_and_class_flag, application_number, class_number = self.check_if_class_and_app_num_in_tag_verification2(
                    keys_not_found_yet, application_number_tag)
            if(app_num_and_class_flag):
                # if true, we can get all the data for application num from excel
                # update that this app_num found
                trademark_data = self.excel.get_trademark_data_by_application_number(
                    self.paper_date, application_number)
                if(trademark_data["type"] == 'Text'):
                    # create txt or image trademark accordint to trademark type
                    try:
                        trademark = self.create_trademark(
                            i, trademark_data, application_number_tag)
                        self.already_done[application_number] = 1
                    except Exception as e:
                        print(e)
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

    def check_if_class_and_app_num_in_tag_verification2(self, keys_not_found_yet, application_number_tag):
        app_num_and_class_flag = False
        numbers = Utils.parse_numbers_from_string(
            application_number_tag.text, self.rows_for_date, keys_not_found_yet)
        for app_num in keys_not_found_yet:
            if(len(numbers) >= 1 and app_num == numbers[0]):
                class_num = self.excel.get_class_by_application_number(
                    self.paper_date, app_num)
                # application number havent been found yet
                app_num_flag = True
                application_number = app_num
                return True, application_number, class_num
        return None, -1, -1

    def create_trademark(self, i, trademark_data, application_number_tag, image_name=None):
        # trademark_type = trademark_data["type"]
        # if(trademark_type == "Text"):
        #     word_to_search = trademark_data["sign"]
        #     text_tag = self.html.extract_text_tag(
        #         word_to_search=word_to_search)
        #     # if it not image
        #     trademark = TextTrademark(
        #         i, text_tag, application_number=trademark_data["application_number"], class_number=trademark_data[
        #             "class_number"], initial_no=trademark_data["initial_no"], date_published=trademark_data["date_published"],
        #         applicant=trademark_data["applicant"], local_agent=trademark_data[
        #             "local_agent"], date_applicated=trademark_data["date_applicated"],
        #     )
        # elif(trademark_type == 'Image'):
        # image_tag = self.html.find_image_tag(
        #     application_number_tag)
        if(image_name is not None):
            trademark = ImageTrademarkXML(
                i, None, image_name, application_number=trademark_data["application_number"], class_number=trademark_data[
                    "class_number"], initial_no=trademark_data["initial_no"], date_published=trademark_data["date_published"],
                applicant=trademark_data["applicant"], local_agent=trademark_data[
                    "local_agent"], date_applicated=trademark_data["date_applicated"],
            )
        else:
            raise Exception(
                "trademark type is not defined text/image")
        trademark.save_trademark(self.file_name)
        self.status_handler.write_to_file(
            trademark.application_number, trademark.index, image_name=trademark.name)
        self.trademarks.append(trademark)
        return trademark

    def extract_text_trademarks_not_found(self):
        for j in list(self.already_done.keys()):
            if(self.already_done[j] == NOT_FOUND):
                try:
                    row = self.excel.get_row_by_application_number(
                        self.paper_date, j)
                    type = Utils.parse_trademark_type(row)
                    if(type == 'Text'):
                        trademark_data = self.excel.get_trademark_data_by_application_number(
                            self.paper_date, j)
                        trademark = self.create_trademark(-2,
                                                          trademark_data, None)
                        self.already_done[int(
                            trademark_data['application_number'])] = 1
                except Exception as e:
                    print(
                        f"extract_text_trademarks_not_found: {j} failed due to: {e}")

    def extract_image_trademarks(self, verification_level=1):
        try:
            self.xml.find_application_numbers_tags_of_images(
                self.images_app_nums_to_search, verification_level=verification_level)
            matches = self.xml.match_between_image_and_app_num()
            for key in matches.keys():
                app_num = key
                if(matches[key] != -1):
                    trademark_data = self.excel.get_trademark_data_by_application_number(
                        self.paper_date, app_num)
                    trademark = self.create_trademark(-1, trademark_data,
                                                      None, image_name=matches[app_num])
                    self.already_done[int(app_num)] = 1
        except Exception as e:
            # rmtree('./'+XML_FOLDER+'/'+self.file_name)
            raise(e)
