from pandas.io import excel
from Consts import PAPERS_FOLDER, PROJECT_PATH
from Trademark import Trademark
import shutil


class ImageTrademark(Trademark):
    def __init__(self, index, tag, application_number=-1, class_number=-1, initial_no=-1, applicant=None, local_agent=None, date_published=None, date_applicated=None):
        super().__init__(index, tag, application_number=application_number, class_number=class_number, initial_no=initial_no,
                         applicant=applicant, local_agent=local_agent, date_published=date_published, date_applicated=date_applicated)
        self.type = "Image"
        self.tag = tag

    def save_trademark(self, folder_name):
        src = self.tag.attrs['src']
        image_location = str(src).split('/')
        save_to = PROJECT_PATH+'/'+PAPERS_FOLDER + \
            '/'+folder_name+'/'+str(self.application_number)+'.png'
        try:
            shutil.copyfile(r'./'+PAPERS_FOLDER + '/' +
                            image_location[0]+'/'+image_location[1], save_to)
            print(
                f"tradmark {self.index} saved as image number {self.application_number}")
        except:
            raise Exception("failed when trying to copy image")
