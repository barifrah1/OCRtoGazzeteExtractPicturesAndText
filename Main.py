import os
from AccuracyCalculator import AccuracyCalculator
from ExcelHandler import ExcelHandler
from Consts import PAPERS_FOLDER, FULL_RUN_MODE
from Paper import Paper
import Utils
from datetime import datetime
import sys
import logging
if __name__ == '__main__':
    d = {}
    excel = ExcelHandler()
    AccuracyCalculator.write_to_accuracy_file(
        '-------'+str(datetime.now())+'---------')
    for file in os.listdir(PAPERS_FOLDER):
        if(Utils.is_docx_file(file) and file == '27-09-01.docx'):
            try:
                logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                                    level=logging.INFO, filename=file.split('.')[0]+'.log')
                paper = Paper(file, excel)
                if(paper.has_real_file):
                    paper.extract_by_real()
                else:
                    paper.extract(verification_level=1)
                    paper.extract(verification_level=1)
                    paper.extract(verification_level=1)
                    paper.extract(verification_level=2)
                    paper.extract(verification_level=2)
                # calculate accuracy
                result = paper.status_handler.read_status_file()
                accuracy_calculator = AccuracyCalculator(
                    file.split('.')[0], result, paper.number_of_rows)
                if(FULL_RUN_MODE):
                    paper.copy_not_found_images()
                    paper.create_verified_file()
                    paper.copy_original_images()
                    excel.write_to_excel(
                        result, paper.paper_date, paper.file_name)
            except Exception as e:
                logging.exception(e)
                print(sys.exc_info()[0].__name__, os.path.basename(sys.exc_info()[
                      2].tb_frame.f_code.co_filename), sys.exc_info()[2].tb_lineno, e)
                continue
