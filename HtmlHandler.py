from Consts import EXCEL_FILE, PAPERS_FOLDER, SHEET_NAME, PROJECT_PATH
import os
import Utils
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz, process
from difflib import SequenceMatcher
import html5lib


class HtmlHandler:
    def __init__(self, fp):
        self.soup = BeautifulSoup(fp, 'html.parser')
        self.body = self.soup.find('body')
        self.head = self.soup.find('head')
        self.style = self.head.find('style')
        self.all_romans = []
        for i in range(1, 100):
            self.all_romans.append(Utils.int_to_Roman(i)+'.')
        self.used_tags = []

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
    def find_roman_number(self, i, verification_level=1):
        roman_number = Utils.int_to_Roman(i)
        roman_tag = self.body.find(lambda tag: tag.name == "span" and (
            (roman_number+'.') in tag.text or (roman_number+',') in tag.text) and len(tag.text) < 8)
        if(roman_tag is None):
            roman_tag = self.body.find(lambda tag: tag.name == "span" and (fuzz.ratio(
                (roman_number+'.'), tag.text) > 90 or (fuzz.ratio(roman_number+',', tag.text) > 90)) and len(tag.text) <= 9)
        if(verification_level == 2):
            roman_tags = self.body.find_all(lambda tag: tag.name == "span" and (
                (roman_number) in tag.text) and len(tag.text) < 8)
            for r in roman_tags:
                if(len(r.text) == len(Utils.int_to_Roman(i))):
                    return r
        return roman_tag

    def find_application_number_tag(self, i, verification_level=1):
        roman_tag = self.find_roman_number(
            i, verification_level=verification_level)
        try:
            if(roman_tag.text[-1] == '.' or roman_tag.text[-1] == ','):
                res = Utils.roman_to_int(roman_tag.text[:-1])
            else:
                res = Utils.roman_to_int(roman_tag.text)
            print(f"{i} detected as: {res}")
            if(i != res):
                print("Wrong i identified for {i}")
                raise Exception(f"Wrong i identified for {i}")
        except:
            print(f"{i} detection failed for {roman_tag.text}")
            raise Exception(f"{i} detection failed for {roman_tag.text}")
        flag = True
        application_tag = None
        application_tag_fuzzy = None
        next = self.find_body_child(roman_tag)
        while(flag):
            # in case that next tag is '\n'
            if(isinstance(next, str) == True):
                next = next.next_sibling
            if(application_tag is None):
                application_tag = next.find(lambda t: t.name == "span" and (
                    ('No.' in t.text or 'No,' in t.text or 'No.' in t.text or 'No ' in t.text) and ('Class' in t.text or 'Clans' in t.text)))
                if(application_tag is None and application_tag_fuzzy is None):
                    application_tag_fuzzy = next.find(lambda t: t.name == "span" and (fuzz.partial_ratio(
                        ('No.').lower(), t.text.lower()) > 65 and fuzz.partial_ratio(('Class').lower(), t.text.lower()) >= 20))
            if(application_tag is not None or application_tag_fuzzy is not None):
                flag = False
            next = next.next_sibling
        if(application_tag is not None):
            return application_tag
        else:
            return application_tag_fuzzy

    def find_application_number_in_body(self, app_num):
        application_tag = self.body.find(lambda t: t.name == "span" and (
            ('No.' in t.text or 'No,' in t.text or 'No ' in t.text) and ('Class' in t.text or 'Clans' in t.text)) and str(app_num) in t.text)
        return application_tag

    def extract_application_number_tag_by_roman(self, i):
        roman_tag = self.find_roman_number(i)
        if(roman_tag is not None):
            application_number_tag = self.find_application_number_tag(
                roman_tag)
        return roman_tag

    def extract_text_tag(self, word_to_search=None):
        if(word_to_search is not None):
            word_to_search = word_to_search.strip()
            text_trade_mark_tag = self.body.find(lambda t: t.name == 'span' and SequenceMatcher(
                None, word_to_search, t.text).ratio() > 0.6)
            if(text_trade_mark_tag == None or text_trade_mark_tag == '<>' or text_trade_mark_tag in self.used_tags):
                raise Exception(
                    "text_trade_mark_tag is empty or not found or already in use")
            else:
                self.used_tags.append(text_trade_mark_tag)
                s = self.build_html_file(text_trade_mark_tag)
                return s

    def find_image_tag(self, application_number_tag):
        image_flag = True
        next = self.find_body_child(application_number_tag)
        while(image_flag):
            if(isinstance(next, str) == True):
                next = next.next_sibling
            else:
                if(next.name == 'img'):
                    image = next
                else:
                    image = next.find(lambda t: t.name == "img")
                if(image != None):
                    if(image in self.used_tags):
                        print("trademark is already used")
                        raise Exception(f"trademark is already used")
                    else:
                        self.used_tags.append(image)
                    return image
                else:
                    next = next.next_sibling

    def find_data_after_image(self, image_tag):
        address_flag = True
        next = self.find_body_child(image_tag)
        while(address_flag):
            if(isinstance(next, str) == True):
                next = next.next_sibling
            else:
                tag = next.find(lambda t: t.name ==
                                'span' and 'address' in t.text.lower())
                if(tag != None):
                    address_tag = tag
                    address_flag = False
                else:
                    next = next.next_sibling
        return address_tag
    # build text tag as html page

    def build_html_file(self, tag):
        s = "<html>"+str(self.head)+"<body>"+str(tag)+"</body></html>"
        return s

    # def build_html_page_for_roman(self, i):
    #     html = u"<html>"+str(self.head)+"<body>"
    #     flag = True
    #     roman_to_search = Utils.int_to_Roman(i)
    #     next_roman = Utils.int_to_Roman(i+1)
    #     current_roman_tag = self.find_roman_number(i)
    #     tag = self.body.find(lambda tag: tag.name == "span" and (
    #         (roman_to_search+'.') in tag.text or (roman_to_search+',') in tag.text) and len(tag.text) < 8)
    #     tag = self.find_body_child(tag)
    #     while(flag):
    #         html += str(tag)
    #         tag = tag.next_sibling
    #         if(isinstance(tag, str) == True):
    #             tag = tag.next_sibling
    #         next_roman = tag.find(lambda tag: tag.name == "span" and (
    #             (next_roman+'.') in tag.text or (next_roman+',') in tag.text) and len(tag.text) < 8)
    #         if(next_roman is not None):
    #             flag = False
    #     html += '</body></html>'
    #     f = open('./html/'+i+'.html', 'wb')
    #     f.write(html)
