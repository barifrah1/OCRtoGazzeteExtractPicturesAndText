import os
from AccuracyCalculator import AccuracyCalculator
from ExcelHandler import ExcelHandler
from Consts import PAPERS_FOLDER
from Paper import Paper
import Utils
from datetime import datetime

if __name__ == '__main__':
    d = {}
    excel = ExcelHandler()
    AccuracyCalculator.write_to_accuracy_file(
        '-------'+str(datetime.now())+'---------')
    for file in os.listdir(PAPERS_FOLDER):
        if(Utils.is_docx_file(file) and file == '36-12-10.docx'):
            try:
                paper = Paper(file, excel)
                paper.extract(verification_level=1)
                paper.extract(verification_level=2)
                # calculate accuracy
                result = paper.status_handler.read_status_file()
                accuracy_calculator = AccuracyCalculator(
                    file.split('.')[0], result)
            except Exception as e:
                print(e)
                continue
