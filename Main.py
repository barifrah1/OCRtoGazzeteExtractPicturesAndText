import os
from ExcelHandler import ExcelHandler
from Consts import PAPERS_FOLDER
from Paper import Paper
import Utils

if __name__ == '__main__':
    d = {}
    excel = ExcelHandler()
    for file in os.listdir(PAPERS_FOLDER):
        if(Utils.is_htm_file(file)):
            try:
                paper = Paper(file, excel)
                paper.extract()
            except Exception as e:
                continue

    # for i in range(1,28):
    #     if(i not in romans_done):
    #         try:
    #             d[i]=extract_image_of_roman_number_i(i)
    #         except Exception as e:
    #             print(i,e, 'failed')
    #     else:
    #         print(f"{i} already done")
    # print(d)
