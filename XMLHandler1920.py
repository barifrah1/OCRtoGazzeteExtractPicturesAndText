import logging
import os
from lxml import etree
from Consts import XML_FOLDER, PAPERS_FOLDER
import pandas as pd
from ExcelHandler import ExcelHandler
import Utils
from shutil import copy, rmtree
from TextHandler import TextHandler
from Filters import Filters
from XMLHandler import XMLHandler


class XMLHandler1920 (XMLHandler):
    def __init__(self, paper_date, rows_for_date):
        super().__init__(paper_date, rows_for_date)

    def get_application_date(self, elem):
        flag = False
        i = 0
        for elem2 in self.tree.iter():
            if(elem2 == elem):
                flag = True
                text = self.get_text_from_paragraph(elem2)

                if(TextHandler.check_is_date_filed_paragraph(text)):
                    date = Utils.get_date_from_text(text)
                    return date
            if(flag != True):
                continue
            else:
                if(elem != elem2 and elem2.tag == self.ns["w"]+'p'):
                    i += 1
                    text = self.get_text_from_paragraph(elem2)
                    text = Utils.clean_text(text)
                    if(TextHandler.check_is_date_filed_paragraph(text)):
                        date = Utils.get_date_from_text(text)
                        return date
            if(i > 3):
                return None
