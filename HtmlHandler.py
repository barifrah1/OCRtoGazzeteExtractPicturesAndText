from Consts import EXCEL_FILE, PAPERS_FOLDER, SHEET_NAME, PROJECT_PATH
import os
import Utils
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz, process
from difflib import SequenceMatcher


class HtmlHandler:
    def __init__(self, fp):
        self.soup = BeautifulSoup(fp, 'html5lib')
        self.body = self.soup.find('body')
        self.head = self.soup.find('head')
        self.style = self.head.find('style')

    # checks wheather or not table tag is the child of body and an ancestor of tag
    def does_table_is_ancestor(self, tag):
        parent = tag
        while(parent.name != 'td'):
            parent = parent.parent
            if(parent.name == 'html'):
                return False
        return True

    # finds the ancestor of tag which is also the child of body, in case of table we want the specific cell in the table
    def find_body_child(self, tag):
        result = self.does_table_is_ancestor(tag)
        if(result):
            flag = tag.parent.name == 'td'
            while(not flag):
                tag = tag.parent
                flag = tag.parent.name == 'td'
        else:
            flag = tag in self.body.children
            while(not flag):
                tag = tag.parent
                flag = tag in self.body.children
        return tag

    # finds tag with roman number(i)
    def find_roman_number(self, i):
        roman_number = Utils.int_to_Roman(i)
        roman_tag = self.body.find(lambda tag: tag.name == "span" and (
            roman_number+'.') in tag.text and len(tag.text) < 8)
        if(roman_tag is None):
            roman_tag = self.body.find(lambda tag: tag.name == "span" and fuzz.ratio(
                (roman_number+'.'), tag.text) > 90 and len(tag.text) <= 9)
        return roman_tag

    def find_application_number_tag(self, roman_tag):
        flag = True
        application_tag = None
        application_tag_fuzzy = None
        next = roman_tag
        while(flag):
            # in case that next tag is '\n'
            if(isinstance(next, str) == True):
                next = next.next_sibling
            if(application_tag is None):
                application_tag = next.find(lambda t: t.name == "span" and (
                    ('No.' in t.text or 'No,' in t.text) and ('Class' in t.text or 'Clans' in t.text)))
                if(application_tag is None and application_tag_fuzzy is None):
                    application_tag_fuzzy = next.find(lambda t: t.name == "span" and (fuzz.partial_ratio(
                        ('No.').lower(), t.text.lower()) > 65 and fuzz.partial_ratio(('Class').lower(), t.text.lower()) >= 20))
            next = next.next_sibling
        if(application_tag is not None):
            return application_tag
        else:
            return application_tag_fuzzy

    def extract_application_number_tag_by_roman(self, i):
        roman_tag = self.find_roman_number(i)
        if(roman_tag is not None):
            application_number_tag = self.find_application_number_tag(
                roman_tag)
        return roman_tag

    def extract_text_tag(self, application_number_tag, word_to_search=None):
        if(word_to_search is not None):
            word_to_search = word_to_search.strip()
            text_trade_mark_tag = self.body.find(lambda t: t.name == 'span' and SequenceMatcher(
                None, word_to_search, t.text).ratio() > 0.6)
            if(text_trade_mark_tag == None or text_trade_mark_tag == '<>'):
                raise Exception("text_trade_mark_tag is empty or not found")
            else:
                s = self.build_html_file(text_trade_mark_tag)
                return s

    def find_image_tag(application_number_tag):
        image_flag = True
        next = application_number_tag.next_sibling
        while(image_flag):
            if(isinstance(next, str) == True):
                next = next.next_sibling
            else:
                if(next.name == 'img'):
                    image = next
                else:
                    image = next.find(lambda t: t.name == "img")
                if(image != None):
                    return image
                    src = image.attrs['src']
                    image_location = str(src).split('/')
                    copy_image(r'auto/'+image_location[0]+'/'+image_location[1],
                               ORIGINAL_DATE_FORMAT+'/'+str(application_number)+'.png')
                    break
                else:
                    next = next.next_sibling

    # build text tag as html page

    def build_html_file(self, tag):
        s = """"
        <html>
        """+str(self.head)+str(tag)+"</html>"
        return s
