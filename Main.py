from datetime import date
import pandas as pd
import imgkit
import os
import shutil
from requests.api import options
from difflib import SequenceMatcher
from fuzzywuzzy import fuzz, process

# new needed
import ExcelHandler
from Consts import PAPERS_FOLDER
from Paper import Paper
from Utils import is_htm_file

if __name__ == '__main__':
    d = {}
    excel = ExcelHandler()
    for file in os.listdir(PAPERS_FOLDER):
        if(is_htm_file(file)):
            paper = Paper(file, excel)
            paper.extract()
    # for i in range(1,28):
    #     if(i not in romans_done):
    #         try:
    #             d[i]=extract_image_of_roman_number_i(i)
    #         except Exception as e:
    #             print(i,e, 'failed')
    #     else:
    #         print(f"{i} already done")
    # print(d)
