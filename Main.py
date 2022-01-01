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
                paper.extract_text_trademarks_not_found()
                paper.extract(verification_level=1)
                paper.extract_by_excel(verification_level=1)
                paper.extract(verification_level=2)
                paper.extract_by_excel(verification_level=2)
                # paper_iteration2 = Paper(file, excel)
                # paper_iteration2.extract(verification_level=2)
            except Exception as e:
                continue
