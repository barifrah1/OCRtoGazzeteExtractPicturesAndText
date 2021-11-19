from pandas.io import excel
from Consts import PAPERS_FOLDER
import pandas as pd
from bs4 import BeautifulSoup
import Utils 
import os
import ExcelHandler
class Trademark:
    def __init__(self,index,application_number=-1,class_no=-1,initial_no=-1,address=None): 
        self.index = index
        self.roman_index = Utils.int_to_Roman(index)
        self.application_number = application_number
        self.class_no = class_no
        self.initial_no = initial_no
        self.address = address
        self.image_path = None

    
      