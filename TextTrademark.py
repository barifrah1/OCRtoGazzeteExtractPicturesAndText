from pandas.io import excel
from Consts import PAPERS_FOLDER, PROJECT_PATH, PATH_WKTHMLTOIMAGE, IMAGE_OPTIONS
import Utils
import os
import Trademark
import imgkit


class TextTrademark(Trademark):
    def __init__(self, index, tag, application_number=-1, class_no=-1, initial_no=-1, applicant=None, local_agent=None, date_published=None, date_applicated=None):
        super().__init__(index, application_number=-application_number, class_no=class_no, initial_no=initial_no,
                         applicant=applicant, local_agent=local_agent, date_published=date_published, date_applicated=date_applicated)
        self.type = "Text"
        self.tag = tag

    def save_trademark(self):
        os.chdir(PROJECT_PATH)
        save_to = PROJECT_PATH+'/'+PAPERS_FOLDER + \
            '/'+str(self.application_number)+'.png'
        try:
            imgkit.from_string(
                self.tag, save_to, config=imgkit.config(wkhtmltoimage=PATH_WKTHMLTOIMAGE), options=IMAGE_OPTIONS)
            self.image_path = save_to
        except Exception as e:
            error_text = "Error when using imgkit for app_num " + self.application_number
            raise Exception(error_text)