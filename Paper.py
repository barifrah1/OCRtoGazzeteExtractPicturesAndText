from pandas.io import excel
from Consts import PAPERS_FOLDER
import pandas as pd
from Trademark import Trademark
import Utils 
import os
import ExcelHandler
import HtmlHandler
class Paper:
    def __init__(self,file,excel): 
        self.file_name = file.split('.')[0]
        self.paper_path = PAPERS_FOLDER+'/'+file
        self.status_path = 'status/'+self.file_name+'.txt'
        self.paper_date = Utils.convert_file_date(self.file_name)
        self.rows_for_date = excel.get_rows_from_date(self.paper_date)
        self.number_of_rows = len(self.rows_for_date)
        #if status folder doesnt exist yet, create it
        if(os.path.exists('status')==False):
            os.mkdir('status')
        # if current file havent been analyzed yet ,extract already finished on empty_mode (no 1's in already done dictionary)
        is_path_exists = os.path.exists('status/'+self.file_name+'.txt')
        self.already_done,self.romans_done = self.get_already_finished(excel,empty_mode= not is_path_exists)
        with open(self.paper_path, encoding="utf8") as fp:
            self.html = HtmlHandler(fp) 
        self.trademarks = []

 
    # get excel file and paper object, return a dictionary with 1 for application numbers that have been already extracted and 0 for the rest
    # return also all roman numbers found
    def get_already_finished(self,excel,empty_mode=False):
        romans = []
        rows = excel[excel["Publication dd//mm/yyyy"]=='OG '+self.paper_date]
        application_numbers = rows["Application No."].values.tolist()
        done = {int(key): 0 for key in application_numbers}
        if(empty_mode==False):
            with open(self.status_path,'r') as f:
                line = f.readline()
                while(line!=''):
                    number = int(line.split('-')[0])
                    roman = int(line.split('-')[1])
                    done[number] = 1
                    romans.append(roman)
                    line = f.readline()
            return done,romans
        else:
            return done,[]
    
    def extract_trademark_by_roman_number(self,i):
        self.html.find_roman_number(i)

    
      