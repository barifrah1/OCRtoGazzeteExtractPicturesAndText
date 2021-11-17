from datetime import date
from bs4 import BeautifulSoup
from numpy.lib.type_check import imag
import pandas as pd
import imgkit
import os
import shutil
from requests.api import options
from difflib import SequenceMatcher
from fuzzywuzzy import fuzz,process

if __name__ == '__main__':
    d={}
    is_exist = os.path.exists(ORIGINAL_DATE_FORMAT)
    if(is_exist== False):
        os.mkdir(ORIGINAL_DATE_FORMAT)
    for i in range(1,28):
        if(i not in romans_done):
            try:
                d[i]=extract_image_of_roman_number_i(i)
            except Exception as e:
                print(i,e, 'failed')
        else:
            print(f"{i} already done")
    print(d)      