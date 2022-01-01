from pandas.io import excel
from Consts import PAPERS_FOLDER, PROJECT_PATH, PATH_WKTHMLTOIMAGE, IMAGE_OPTIONS
import Utils
import os
from Trademark import Trademark
import imgkit


class TextTrademark(Trademark):
    def __init__(self, index, tag, application_number=-1, class_number=-1, initial_no=-1, applicant=None, local_agent=None, date_published=None, date_applicated=None):
        super().__init__(index, tag, application_number=application_number, class_number=class_number, initial_no=initial_no,
                         applicant=applicant, local_agent=local_agent, date_published=date_published, date_applicated=date_applicated)
        self.type = "Text"
        self.tag = tag

    def save_trademark(self, folder_name):
        save_to = PROJECT_PATH+'/'+PAPERS_FOLDER + \
            '/'+folder_name+'/'+str(self.application_number)+'.png'
        Utils.create_folder_if_not_exist('./'+PAPERS_FOLDER+'/'+folder_name)
        try:
            imgkit.from_string(
                self.tag, save_to, config=imgkit.config(wkhtmltoimage=PATH_WKTHMLTOIMAGE), options=IMAGE_OPTIONS)
            self.image_path = save_to
            print(
                f"trademark {self.index} saved as TextTrademark application number: {self.application_number}")
        except Exception as e:
            error_text = "Error when using imgkit for app_num " + self.application_number
            raise Exception(error_text)
